import "dotenv/config";
import express from "express";
import rateLimit from "express-rate-limit";
import { randomUUID } from "node:crypto";
import { findMatchingPayment } from "../lib/stellar.js";
import { supabase } from "../lib/supabase.js";
import { validateUuidParam } from "../lib/validate-uuid.js";
import { paymentZodSchema } from "../lib/request-schemas.js";
import { createCreatePaymentRateLimit } from "../lib/create-payment-rate-limit.js";
import { sendWebhook } from "../lib/webhooks.js";

const createPaymentRateLimit = createCreatePaymentRateLimit();

const defaultVerifyPaymentRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: { error: "Too many verification requests, please try again later." },
  standardHeaders: true,
  legacyHeaders: false,
});

function createPaymentsRouter({
  verifyPaymentRateLimit = defaultVerifyPaymentRateLimit,
} = {}) {
  const router = express.Router();

  /**
   * @swagger
   * /api/create-payment:
   *   post:
   *     summary: Create a new payment request
   *     tags: [Payments]
   *     parameters:
   *       - in: header
   *         name: Idempotency-Key
   *         schema:
   *           type: string
   *         description: Optional unique key for idempotent requests. Use UUID or request ID. Responses are cached for 24 hours.
   *     requestBody:
   *       required: true
   *       content:
   *         application/json:
   *           schema:
   *             type: object
   *             required: [amount, asset, recipient]
   *             properties:
   *               amount:
   *                 type: number
   *                 description: Payment amount (must be positive and at least 0.01 XLM for native payments)
   *               asset:
   *                 type: string
   *                 description: Asset code (e.g. XLM, USDC)
   *               asset_issuer:
   *                 type: string
   *                 description: Asset issuer (required for non-native assets)
   *               recipient:
   *                 type: string
   *                 description: Stellar address of the recipient
   *               merchant_id:
   *                 type: string
   *               description:
   *                 type: string
   *               memo:
   *                 type: string
   *               memo_type:
   *                 type: string
   *                 enum: [text, id, hash, return]
   *               webhook_url:
   *                 type: string
   *     responses:
   *       201:
   *         description: Payment created
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 payment_id:
   *                   type: string
   *                 payment_link:
   *                   type: string
   *                 status:
   *                   type: string
   *       200:
   *         description: Duplicate request — cached response returned from idempotency key
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 payment_id:
   *                   type: string
   *                 payment_link:
   *                   type: string
   *                 status:
   *                   type: string
   *       400:
   *         description: Validation error or invalid Idempotency-Key
   *       429:
   *         description: Too many requests
   */
  router.post("/create-payment", createPaymentRateLimit, async (req, res, next) => {
    try {
      const body = paymentZodSchema.parse(req.body || {});

      const paymentId = randomUUID();
      const now = new Date().toISOString();
      const paymentLinkBase =
        process.env.PAYMENT_LINK_BASE || "http://localhost:3000";
      const paymentLink = `${paymentLinkBase}/pay/${paymentId}`;

      const payload = {
        id: paymentId,
        merchant_id: req.merchant.id,
        amount: body.amount,
        asset: body.asset,
        asset_issuer: body.asset_issuer || null,
        recipient: body.recipient,
        description: body.description || null,
        memo: body.memo || null,
        memo_type: body.memo_type || null,
        webhook_url: body.webhook_url || null,
        status: "pending",
        tx_id: null,
        metadata: body.metadata || null,
        created_at: now,
      };

      const { error: insertError } = await supabase.from("payments").insert(payload);

      if (insertError) {
        insertError.status = 500;
        throw insertError;
      }

      res.status(201).json({
        payment_id: paymentId,
        payment_link: paymentLink,
        status: "pending",
      });
    } catch (err) {
      next(err);
    }
  });

  /**
   * @swagger
   * /api/payment-status/{id}:
   *   get:
   *     summary: Get the status of a payment
   *     tags: [Payments]
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: string
   *         description: Payment ID
   *     responses:
   *       200:
   *         description: Payment details
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 payment:
   *                   type: object
   *       404:
   *         description: Payment not found
   */
  router.get("/payment-status/:id", validateUuidParam(), async (req, res, next) => {
    try {
      const { data, error } = await supabase
        .from("payments")
        .select(
          "id, amount, asset, asset_issuer, recipient, description, memo, memo_type, status, tx_id, metadata, created_at",
        )
        .eq("id", req.params.id)
        .maybeSingle();

      if (error) {
        error.status = 500;
        throw error;
      }

      if (!data) {
        return res.status(404).json({ error: "Payment not found" });
      }

      res.json({ payment: data });
    } catch (err) {
      next(err);
    }
  });

  /**
   * @swagger
   * /api/verify-payment/{id}:
   *   post:
   *     summary: Verify a payment on the Stellar network
   *     tags: [Payments]
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: string
   *         description: Payment ID
   *     responses:
   *       200:
   *         description: Verification result
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 status:
   *                   type: string
   *                   enum: [pending, confirmed]
   *                 tx_id:
   *                   type: string
   *                 webhook:
   *                   type: object
   *       404:
   *         description: Payment not found
   */
  router.post(
    "/verify-payment/:id",
    verifyPaymentRateLimit,
    validateUuidParam(),
    async (req, res, next) => {
      try {
        const { data, error } = await supabase
          .from("payments")
          .select(
            "id, amount, asset, asset_issuer, recipient, status, tx_id, memo, memo_type, webhook_url, merchants(webhook_secret)",
          )
          .eq("id", req.params.id)
          .maybeSingle();

        if (error) {
          error.status = 500;
          throw error;
        }

        if (!data) {
          return res.status(404).json({ error: "Payment not found" });
        }

        if (data.status === "confirmed") {
          return res.json({
            status: "confirmed",
            tx_id: data.tx_id,
            ledger_url: `https://stellar.expert/explorer/testnet/tx/${data.tx_id}`,
          });
        }

        const match = await findMatchingPayment({
          recipient: data.recipient,
          amount: data.amount,
          assetCode: data.asset,
          assetIssuer: data.asset_issuer,
          memo: data.memo,
          memoType: data.memo_type,
        });

        if (!match) {
          return res.json({ status: "pending" });
        }

        const { error: updateError } = await supabase
          .from("payments")
          .update({ status: "confirmed", tx_id: match.transaction_hash })
          .eq("id", data.id);

        if (updateError) {
          updateError.status = 500;
          throw updateError;
        }

        const merchantSecret = data.merchants?.webhook_secret;

        const webhookResult = await sendWebhook(
          data.webhook_url,
          {
            event: "payment.confirmed",
            payment_id: data.id,
            amount: data.amount,
            asset: data.asset,
            asset_issuer: data.asset_issuer,
            recipient: data.recipient,
            tx_id: match.transaction_hash,
          },
          merchantSecret,
        );

        if (!webhookResult.ok && !webhookResult.skipped) {
          console.warn("Webhook failed", webhookResult);
        }

        res.json({
          status: "confirmed",
          tx_id: match.transaction_hash,
          ledger_url: `https://stellar.expert/explorer/testnet/tx/${match.transaction_hash}`,
          webhook: webhookResult,
        });
      } catch (err) {
        next(err);
      }
    },
  );

  /**
   * @swagger
   * /api/payments:
   *   get:
   *     summary: Get paginated list of payments for the authenticated merchant
   *     tags: [Payments]
   *     security:
   *       - ApiKeyAuth: []
   *     parameters:
   *       - in: query
   *         name: page
   *         schema:
   *           type: integer
   *           default: 1
   *         description: Page number (1-indexed)
   *       - in: query
   *         name: limit
   *         schema:
   *           type: integer
   *           default: 10
   *         description: Number of results per page (max 100)
   *     responses:
   *       200:
   *         description: Paginated payments
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 payments:
   *                   type: array
   *                   items:
   *                     type: object
   *                 total_count:
   *                   type: integer
   *                 total_pages:
   *                   type: integer
   *                 page:
   *                   type: integer
   *                 limit:
   *                   type: integer
   *       401:
   *         description: Missing or invalid API key
   */
  router.get("/payments", async (req, res, next) => {
    try {
      let page = parseInt(req.query.page, 10) || 1;
      let limit = parseInt(req.query.limit, 10) || 10;

      if (page < 1) page = 1;
      if (limit < 1) limit = 1;
      if (limit > 100) limit = 100;

      const offset = (page - 1) * limit;

      const { count: totalCount, error: countError } = await supabase
        .from("payments")
        .select("*", { count: "exact", head: true })
        .eq("merchant_id", req.merchant.id);

      if (countError) {
        countError.status = 500;
        throw countError;
      }

      const { data: payments, error: dataError } = await supabase
        .from("payments")
        .select(
          "id, amount, asset, asset_issuer, recipient, description, status, tx_id, created_at",
        )
        .eq("merchant_id", req.merchant.id)
        .order("created_at", { ascending: false })
        .range(offset, offset + limit - 1);

      if (dataError) {
        dataError.status = 500;
        throw dataError;
      }

      const totalPages = Math.ceil(totalCount / limit);

      res.json({
        payments: payments || [],
        total_count: totalCount,
        total_pages: totalPages,
        page,
        limit,
      });
    } catch (err) {
      next(err);
    }
  });

  /**
   * @swagger
   * /api/metrics/7day:
   *   get:
   *     summary: Get 7-day rolling payment volume metrics
   *     tags: [Metrics]
   *     security:
   *       - ApiKeyAuth: []
   *     responses:
   *       200:
   *         description: Daily volume data for past 7 days
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 data:
   *                   type: array
   *                   items:
   *                     type: object
   *                     properties:
   *                       date:
   *                         type: string
   *                         description: Date in YYYY-MM-DD format
   *                       volume:
   *                         type: number
   *                         description: Total payment amount for that day
   *                       count:
   *                         type: integer
   *                         description: Number of payments on that day
   *                 total_volume:
   *                   type: number
   *                   description: Total volume across all 7 days
   *                 total_payments:
   *                   type: integer
   *                   description: Total payment count across all 7 days
   *       401:
   *         description: Missing or invalid API key
   */
  router.get("/metrics/7day", async (req, res, next) => {
    try {
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

      const { data: payments, error } = await supabase
        .from("payments")
        .select("amount, created_at, status")
        .eq("merchant_id", req.merchant.id)
        .gte("created_at", sevenDaysAgo.toISOString())
        .order("created_at", { ascending: true });

      if (error) {
        error.status = 500;
        throw error;
      }

      const metricsMap = new Map();
      let totalVolume = 0;

      payments.forEach((payment) => {
        const date = new Date(payment.created_at).toISOString().split("T")[0];
        const volume = Number(payment.amount) || 0;

        if (!metricsMap.has(date)) {
          metricsMap.set(date, { date, volume: 0, count: 0 });
        }

        const dayMetric = metricsMap.get(date);
        dayMetric.volume += volume;
        dayMetric.count += 1;
        totalVolume += volume;
      });

      const data = [];
      for (let i = 6; i >= 0; i -= 1) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split("T")[0];

        if (metricsMap.has(dateStr)) {
          data.push(metricsMap.get(dateStr));
        } else {
          data.push({ date: dateStr, volume: 0, count: 0 });
        }
      }

      res.json({
        data,
        total_volume: Number(totalVolume.toFixed(2)),
        total_payments: payments.length,
      });
    } catch (err) {
      next(err);
    }
  });

  return router;
}

export default createPaymentsRouter;
