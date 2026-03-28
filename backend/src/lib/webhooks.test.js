import { describe, expect, it } from "vitest";
import { signPayload, verifyWebhook } from "./webhooks.js";

describe("verifyWebhook", () => {
  it("accepts signatures generated with the current webhook secret", () => {
    const rawBody = JSON.stringify({ event: "payment.confirmed", amount: "10" });
    const merchant = {
      webhook_secret: "current-secret",
      webhook_secret_old: null,
      webhook_secret_expiry: null,
    };

    const signature = signPayload(rawBody, merchant.webhook_secret);

    expect(verifyWebhook(rawBody, `sha256=${signature}`, merchant)).toBe(true);
  });

  it("accepts signatures generated with old secret before expiry", () => {
    const rawBody = JSON.stringify({ event: "payment.confirmed", amount: "10" });
    const merchant = {
      webhook_secret: "current-secret",
      webhook_secret_old: "old-secret",
      webhook_secret_expiry: new Date(Date.now() + 60_000).toISOString(),
    };

    const signature = signPayload(rawBody, merchant.webhook_secret_old);

    expect(verifyWebhook(rawBody, `sha256=${signature}`, merchant)).toBe(true);
  });

  it("rejects signatures generated with old secret after expiry", () => {
    const rawBody = JSON.stringify({ event: "payment.confirmed", amount: "10" });
    const merchant = {
      webhook_secret: "current-secret",
      webhook_secret_old: "old-secret",
      webhook_secret_expiry: new Date(Date.now() - 60_000).toISOString(),
    };

    const signature = signPayload(rawBody, merchant.webhook_secret_old);

    expect(verifyWebhook(rawBody, `sha256=${signature}`, merchant)).toBe(false);
  });

  it("rejects malformed signature headers", () => {
    const rawBody = JSON.stringify({ event: "payment.confirmed", amount: "10" });
    const merchant = {
      webhook_secret: "current-secret",
      webhook_secret_old: null,
      webhook_secret_expiry: null,
    };

    expect(verifyWebhook(rawBody, "invalid", merchant)).toBe(false);
  });
});
