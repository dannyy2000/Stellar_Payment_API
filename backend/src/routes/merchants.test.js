import { beforeEach, describe, expect, it, vi } from "vitest";

const eq = vi.fn();
const update = vi.fn(() => ({ eq }));
const from = vi.fn(() => ({ update }));

vi.mock("../lib/supabase.js", () => ({
  supabase: { from },
}));

function createResponse() {
  return {
    status: vi.fn(),
    json: vi.fn(),
  };
}

function getRotateWebhookSecretHandler(router) {
  const layer = router.stack.find(
    (entry) =>
      entry.route?.path === "/merchants/rotate-webhook-secret" &&
      entry.route?.methods?.post,
  );

  if (!layer) {
    throw new Error("rotate-webhook-secret route not found");
  }

  return layer.route.stack[0].handle;
}

describe("POST /api/merchants/rotate-webhook-secret", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    delete process.env.WEBHOOK_SECRET_ROTATION_GRACE_HOURS;
    eq.mockResolvedValue({ error: null });
  });

  it("rotates secret with default 24h grace period", async () => {
    const { default: router } = await import("./merchants.js");
    const handler = getRotateWebhookSecretHandler(router);

    const req = {
      body: {},
      merchant: {
        id: "merchant-123",
        webhook_secret: "whsec_old_secret",
      },
    };

    const res = createResponse();
    const next = vi.fn();

    const nowBefore = Date.now();
    await handler(req, res, next);
    const nowAfter = Date.now();

    expect(from).toHaveBeenCalledWith("merchants");
    expect(update).toHaveBeenCalledTimes(1);

    const updatePayload = update.mock.calls[0][0];
    expect(updatePayload.webhook_secret_old).toBe("whsec_old_secret");
    expect(updatePayload.webhook_secret).toMatch(/^whsec_[a-f0-9]{64}$/);

    const expiry = new Date(updatePayload.webhook_secret_expiry).getTime();
    const lowerBound = nowBefore + 24 * 60 * 60 * 1000;
    const upperBound = nowAfter + 24 * 60 * 60 * 1000 + 1_000;
    expect(expiry).toBeGreaterThanOrEqual(lowerBound);
    expect(expiry).toBeLessThanOrEqual(upperBound);

    expect(eq).toHaveBeenCalledWith("id", "merchant-123");
    expect(res.json).toHaveBeenCalledTimes(1);

    const responsePayload = res.json.mock.calls[0][0];
    expect(responsePayload.webhook_secret).toMatch(/^whsec_[a-f0-9]{64}$/);
    expect(responsePayload.grace_period_hours).toBe(24);
    expect(next).not.toHaveBeenCalled();
  });

  it("uses request grace period override", async () => {
    const { default: router } = await import("./merchants.js");
    const handler = getRotateWebhookSecretHandler(router);

    const req = {
      body: { grace_period_hours: 2 },
      merchant: {
        id: "merchant-123",
        webhook_secret: "whsec_old_secret",
      },
    };

    const res = createResponse();
    const next = vi.fn();

    const nowBefore = Date.now();
    await handler(req, res, next);
    const nowAfter = Date.now();

    const updatePayload = update.mock.calls[0][0];
    const expiry = new Date(updatePayload.webhook_secret_expiry).getTime();
    const lowerBound = nowBefore + 2 * 60 * 60 * 1000;
    const upperBound = nowAfter + 2 * 60 * 60 * 1000 + 1_000;

    expect(expiry).toBeGreaterThanOrEqual(lowerBound);
    expect(expiry).toBeLessThanOrEqual(upperBound);

    const responsePayload = res.json.mock.calls[0][0];
    expect(responsePayload.grace_period_hours).toBe(2);
    expect(next).not.toHaveBeenCalled();
  });
});
