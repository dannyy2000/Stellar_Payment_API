import request from "supertest";
import { createApp } from "../../src/app.js";
import { closePool } from "../../src/lib/db.js";

const mockRedisClient = {
  ping: jest.fn().mockResolvedValue("PONG"),
  on: jest.fn(),
};

describe("Prometheus Metrics", () => {
  let app;
  let io;

  beforeAll(async () => {
    ({ app, io } = await createApp({ redisClient: mockRedisClient }));
  });

  afterAll(async () => {
    if (io) io.close();
    await closePool();
  });

  it("GET /metrics responds 200 and includes default metrics", async () => {
    const res = await request(app).get("/metrics");

    expect(res.status).toBe(200);
    expect(res.text).toContain("process_cpu_seconds_total");
    expect(res.text).toContain("nodejs_version_info");
  });

  it("GET /metrics includes custom payment counters", async () => {
    const res = await request(app).get("/metrics");

    expect(res.status).toBe(200);
    expect(res.text).toContain("payment_created_total");
    expect(res.text).toContain("payment_confirmed_total");
    expect(res.text).toContain("payment_failed_total");
    expect(res.text).toContain("payment_confirmation_latency_seconds");
  });
});
