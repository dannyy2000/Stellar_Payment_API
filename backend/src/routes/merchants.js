import express from "express";
import { randomBytes } from "crypto";
import { supabase } from "../lib/supabase.js";

const router = express.Router();

const REQUIRED_FIELDS = ["email", "business_name", "notification_email"];

function validateRegisterMerchant(body) {
  for (const field of REQUIRED_FIELDS) {
    if (!body[field]) {
      return `Missing field: ${field}`;
    }
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(body.email)) {
    return "Invalid email format";
  }
  if (!emailRegex.test(body.notification_email)) {
    return "Invalid notification_email format";
  }

  return null;
}

/**
 * POST /register
 * Creates a new merchant profile and returns an API key.
 */
router.post("/register", async (req, res, next) => {
  try {
    const error = validateRegisterMerchant(req.body || {});
    if (error) {
      return res.status(400).json({ error });
    }

    const { email, business_name, notification_email } = req.body;

    // Check if merchant already exists
    const { data: existing } = await supabase
      .from("merchants")
      .select("id")
      .eq("email", email)
      .maybeSingle();

    if (existing) {
      return res.status(409).json({ error: "Merchant with this email already exists" });
    }

    // Generate secure credentials
    const apiKey = `sk_${randomBytes(24).toString("hex")}`;
    const webhookSecret = `whsec_${randomBytes(24).toString("hex")}`;

    const payload = {
      email,
      business_name,
      notification_email,
      api_key: apiKey,
      webhook_secret: webhookSecret,
      created_at: new Date().toISOString()
    };

    const { data: merchant, error: insertError } = await supabase
      .from("merchants")
      .insert(payload)
      .select()
      .single();

    if (insertError) {
      insertError.status = 500;
      throw insertError;
    }

    res.status(201).json({
      message: "Merchant registered successfully",
      merchant: {
        id: merchant.id,
        email: merchant.email,
        business_name: merchant.business_name,
        notification_email: merchant.notification_email,
        api_key: merchant.api_key,
        webhook_secret: merchant.webhook_secret,
        created_at: merchant.created_at
      }
    });
  } catch (err) {
    next(err);
  }
});

export default router;
