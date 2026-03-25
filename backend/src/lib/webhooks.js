import { createHmac } from "crypto";

const RETRY_DELAYS_MS = [10_000, 30_000, 60_000]; // 10s, 30s, 60s

/**
 * Signs a serialized payload string with HMAC-SHA256 using the shared secret.
 */
export function signPayload(rawBody, secret) {
  return createHmac("sha256", secret).update(rawBody).digest("hex");
}

async function attempt(url, payload, headers) {
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  const text = await response.text().catch(() => "");
  return { ok: response.ok, status: response.status, body: text };
}

function scheduleRetries(url, payload, headers) {
  let attemptIndex = 0;

  function retry() {
    attempt(url, payload, headers).then((result) => {
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
export async function sendWebhook(url, payload, secret) {
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
    const result = await attempt(url, payload, headers);

    if (!result.ok) {
      console.warn(`Webhook to ${url} failed with status ${result.status}. Scheduling retries.`);
      scheduleRetries(url, payload, headers);
    }

    return { ...result, signed: !!signingSecret };
  } catch (err) {
    console.error(`Webhook to ${url} encountered an error: ${err.message}. Scheduling retries.`);
    scheduleRetries(url, payload, headers);
    return { ok: false, error: err.message, signed: !!signingSecret };
  }
}
