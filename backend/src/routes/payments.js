import express from "express";
import { randomUUID } from "crypto";
import { supabase } from "../lib/supabase.js";
import { findMatchingPayment } from "../lib/stellar.js";
import { sendWebhook } from "../lib/webhooks.js";

const router = express.Router();

const REQUIRED_FIELDS = ["amount", "asset", "recipient"];

function validateCreatePayment(body) {
  for (const field of REQUIRED_FIELDS) {
    if (!body[field]) {
      return `Missing field: ${field}`;
    }
  }

  if (Number.isNaN(Number(body.amount)) || Number(body.amount) <= 0) {
    return "Amount must be a positive number";
  }

  const asset = String(body.asset || "").toUpperCase();
  const hasIssuer =
    body.asset_issuer || (asset === "USDC" && process.env.USDC_ISSUER);
  if (asset !== "XLM" && !hasIssuer) {
    return "asset_issuer is required for non-native assets";
  }

  return null;
}

router.post("/create-payment", async (req, res, next) => {
  try {
    const error = validateCreatePayment(req.body || {});
    if (error) {
      return res.status(400).json({ error });
    }

    const paymentId = randomUUID();
    const now = new Date().toISOString();
    const paymentLinkBase = process.env.PAYMENT_LINK_BASE || "http://localhost:3000";
    const paymentLink = `${paymentLinkBase}/pay/${paymentId}`;

    const asset = String(req.body.asset || "").toUpperCase();
    const assetIssuer =
      req.body.asset_issuer ||
      (asset === "USDC" ? process.env.USDC_ISSUER : null);

    const payload = {
      id: paymentId,
      merchant_id: req.body.merchant_id || null,
      amount: Number(req.body.amount),
      asset,
      asset_issuer: assetIssuer,
      recipient: req.body.recipient,
      description: req.body.description || null,
      webhook_url: req.body.webhook_url || null,
      status: "pending",
      tx_id: null,
      created_at: now
    };

    const { error: insertError } = await supabase
      .from("payments")
      .insert(payload);

    if (insertError) {
      insertError.status = 500;
      throw insertError;
    }

    res.status(201).json({
      payment_id: paymentId,
      payment_link: paymentLink,
      status: "pending"
    });
  } catch (err) {
    next(err);
  }
});

router.get("/payment-status/:id", async (req, res, next) => {
  try {
    const { data, error } = await supabase
      .from("payments")
      .select(
        "id, amount, asset, asset_issuer, recipient, description, status, tx_id, created_at"
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

router.post("/verify-payment/:id", async (req, res, next) => {
  try {
    const { data, error } = await supabase
      .from("payments")
      .select(
        "id, amount, asset, asset_issuer, recipient, status, tx_id, webhook_url, merchants(webhook_secret)"
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
      return res.json({ status: "confirmed", tx_id: data.tx_id });
    }

    const match = await findMatchingPayment({
      recipient: data.recipient,
      amount: data.amount,
      assetCode: data.asset,
      assetIssuer: data.asset_issuer
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

    const webhookResult = await sendWebhook(data.webhook_url, {
      event: "payment.confirmed",
      payment_id: data.id,
      amount: data.amount,
      asset: data.asset,
      asset_issuer: data.asset_issuer,
      recipient: data.recipient,
      tx_id: match.transaction_hash
    }, merchantSecret);

    if (!webhookResult.ok && !webhookResult.skipped) {
      console.warn("Webhook failed", webhookResult);
    }

    res.json({
      status: "confirmed",
      tx_id: match.transaction_hash,
      webhook: webhookResult
    });
  } catch (err) {
    next(err);
  }
});

export default router;
