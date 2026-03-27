import 'dotenv/config';
import { createHmac, timingSafeEqual } from "crypto";
import { supabase } from "./supabase.js";

const RETRY_DELAYS_MS = [10_000, 30_000, 60_000]; // 10s, 30s, 60s

/**
 * Signs a serialized payload string with HMAC-SHA256 using the shared secret.
 */
export function signPayload(rawBody, secret) {
  return createHmac("sha256", secret).update(rawBody).digest("hex");
}

function parseSignatureHeader(signatureHeader) {
  if (typeof signatureHeader !== "string") return null;

  const trimmed = signatureHeader.trim();
  if (!trimmed.startsWith("sha256=")) return null;

  const signature = trimmed.slice("sha256=".length);
  if (!/^[a-f0-9]{64}$/i.test(signature)) return null;

  return signature.toLowerCase();
}

function signaturesEqual(a, b) {
  const aBuffer = Buffer.from(a, "utf8");
  const bBuffer = Buffer.from(b, "utf8");

  if (aBuffer.length !== bBuffer.length) return false;
  return timingSafeEqual(aBuffer, bBuffer);
}

/**
 * Verifies a Stellar-Signature header against the merchant webhook secrets.
 * Accepts the current secret and, during grace window, the previous secret.
 */
export function verifyWebhook(rawBody, signatureHeader, merchant) {
  const signature = parseSignatureHeader(signatureHeader);
  if (!signature || !merchant || !merchant.webhook_secret) return false;

  const candidateSecrets = [merchant.webhook_secret];
  if (merchant.webhook_secret_old && merchant.webhook_secret_expiry) {
    const expiry = new Date(merchant.webhook_secret_expiry);
    if (!Number.isNaN(expiry.getTime()) && expiry.getTime() > Date.now()) {
      candidateSecrets.push(merchant.webhook_secret_old);
    }
  }

  return candidateSecrets.some((secret) => {
    const expected = signPayload(rawBody, secret);
    return signaturesEqual(signature, expected);
  });
}

/**
 * Log webhook delivery attempt to database
 */
async function logWebhookDelivery(paymentId, statusCode, responseBody) {
  if (!paymentId) return;

  try {
    await supabase.from("webhook_delivery_logs").insert({
      payment_id: paymentId,
      status_code: statusCode,
      response_body: responseBody ? responseBody.substring(0, 1000) : null // Limit response body size
    });
  } catch (err) {
    console.error("Failed to log webhook delivery:", err.message);
  }
}

async function attempt(url, payload, headers, paymentId) {
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  const text = await response.text().catch(() => "");
  
  // Log the delivery attempt
  await logWebhookDelivery(paymentId, response.status, text);
  
  return { ok: response.ok, status: response.status, body: text };
}

function scheduleRetries(url, payload, headers, paymentId) {
  let attemptIndex = 0;

  function retry() {
    attempt(url, payload, headers, paymentId).then((result) => {
      if (!result.ok && attemptIndex < RETRY_DELAYS_MS.length) {
        const delay = RETRY_DELAYS_MS[attemptIndex];
        attemptIndex++;
        console.log(`Webhook retry ${attemptIndex} for ${url} in ${delay}ms`);
        setTimeout(retry, delay);
      }
    }).catch((err) => {
      if (attemptIndex < RETRY_DELAYS_MS.length) {
        const delay = RETRY_DELAYS_MS[attemptIndex];
        attemptIndex++;
        console.warn(`Webhook retry ${attemptIndex} (error) for ${url} in ${delay}ms:`, err.message);
        setTimeout(retry, delay);
      }
    });
  }

  setTimeout(retry, RETRY_DELAYS_MS[0]);
}

/**
 * Sends a signed webhook POST request to `url`.
 */
export async function sendWebhook(url, payload, secret, paymentId = null) {
  if (!url) return { ok: false, skipped: true };

  const signingSecret = secret || process.env.WEBHOOK_SECRET || "";
  const rawBody = JSON.stringify(payload);

  const headers = {
    "Content-Type": "application/json",
    "User-Agent": "stellar-payment-api/0.1"
  };

  if (signingSecret) {
    const signature = signPayload(rawBody, signingSecret);
    headers["Stellar-Signature"] = `sha256=${signature}`;
  }

  try {
    const result = await attempt(url, payload, headers, paymentId);

    if (!result.ok) {
      console.warn(`Webhook to ${url} failed with status ${result.status}. Scheduling retries.`);
      scheduleRetries(url, payload, headers, paymentId);
    }

    return { ...result, signed: !!signingSecret };
  } catch (err) {
    console.error(`Webhook to ${url} encountered an error: ${err.message}. Scheduling retries.`);
    
    // Log the error
    if (paymentId) {
      await logWebhookDelivery(paymentId, 0, err.message);
    }
    
    scheduleRetries(url, payload, headers, paymentId);
    return { ok: false, error: err.message, signed: !!signingSecret };
  }
}
