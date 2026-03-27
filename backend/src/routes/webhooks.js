import express from "express";
import { supabase } from "../lib/supabase.js";
import { sendWebhook } from "../lib/webhooks.js";

const router = express.Router();

/**
 * @swagger
 * /api/webhooks/logs:
 *   get:
 *     summary: Get webhook delivery logs for authenticated merchant
 *     tags: [Webhooks]
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
 *           default: 20
 *           maximum: 100
 *         description: Number of logs per page
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [success, failure]
 *         description: Filter by success (2xx) or failure (non-2xx)
 *     responses:
 *       200:
 *         description: Paginated webhook logs
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 logs:
 *                   type: array
 *                 pagination:
 *                   type: object
 *                   properties:
 *                     page:
 *                       type: integer
 *                     limit:
 *                       type: integer
 *                     total:
 *                       type: integer
 *                     totalPages:
 *                       type: integer
 */
router.get("/webhooks/logs", async (req, res, next) => {
  try {
    const merchantId = req.merchant.id;
    
    // Parse pagination params
    const page = Math.max(1, parseInt(req.query.page) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || 20));
    const offset = (page - 1) * limit;
    
    // Build query
    let query = supabase
      .from("webhook_delivery_logs")
      .select(`
        id,
        payment_id,
        status_code,
        response_body,
        timestamp,
        payments!inner(merchant_id, amount, asset, status)
      `, { count: 'exact' })
      .eq("payments.merchant_id", merchantId)
      .order("timestamp", { ascending: false });
    
    // Filter by status if provided
    if (req.query.status === 'success') {
      query = query.gte("status_code", 200).lt("status_code", 300);
    } else if (req.query.status === 'failure') {
      query = query.or("status_code.lt.200,status_code.gte.300");
    }
    
    // Apply pagination
    query = query.range(offset, offset + limit - 1);
    
    const { data, error, count } = await query;
    
    if (error) {
      error.status = 500;
      throw error;
    }
    
    // Format response
    const logs = data.map(log => ({
      id: log.id,
      payment_id: log.payment_id,
      status_code: log.status_code,
      success: log.status_code >= 200 && log.status_code < 300,
      response_body: log.response_body,
      timestamp: log.timestamp,
      payment: {
        amount: log.payments.amount,
        asset: log.payments.asset,
        status: log.payments.status
      }
    }));
    
    res.json({
      logs,
      pagination: {
        page,
        limit,
        total: count || 0,
        totalPages: Math.ceil((count || 0) / limit)
      }
    });
  } catch (err) {
    next(err);
  }
});

/**
 * @swagger
 * /api/webhooks/test:
 *   post:
 *     summary: Send a test webhook to the merchant's stored webhook URL
 *     tags: [Webhooks]
 *     security:
 *       - ApiKeyAuth: []
 *     responses:
 *       200:
 *         description: Test webhook dispatched
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 ok:
 *                   type: boolean
 *                 status:
 *                   type: integer
 *                 body:
 *                   type: string
 *                 signed:
 *                   type: boolean
 *       400:
 *         description: No webhook URL configured
 *       401:
 *         description: Missing or invalid API key
 */

router.post("/webhooks/test", async (req, res, next) => {
  try {
    // 1. Fetch the merchant's webhook_url and webhook_secret from DB
    const { data: merchant, error } = await supabase
      .from("merchants")
      .select("webhook_url, webhook_secret")
      .eq("id", req.merchant.id)
      .maybeSingle();

    if (error) {
      error.status = 500;
      throw error;
    }

    // 2. Guard: merchant must have a webhook URL saved
    if (!merchant?.webhook_url) {
      return res.status(400).json({
        error: "No webhook URL configured for this merchant.",
      });
    }

    // 3. Build a dummy payload mimicking a real payment.confirmed event
    const dummyPayload = {
      event: "payment.confirmed",
      test: true,
      payment_id: "00000000-0000-0000-0000-000000000000",
      amount: "1.00",
      asset: "XLM",
      asset_issuer: null,
      recipient: "GAAZI4TCR3TY5OJHCTJC2A4QSY6CJWJH5IAJTGKIN2ER7LBNVKOCCWN",
      tx_id: "test_tx_abc123",
    };

    // 4. Send the webhook using the existing sendWebhook utility
    const result = await sendWebhook(
      merchant.webhook_url,
      dummyPayload,
      merchant.webhook_secret
    );

    // 5. Return the result
    res.json({
      ok: result.ok,
      status: result.status,
      body: result.body,
      signed: result.signed,
    });
  } catch (err) {
    next(err);
  }
});

export default router;