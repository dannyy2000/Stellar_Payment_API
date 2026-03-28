import express from "express";
import { register } from "../lib/metrics.js";

const router = express.Router();

/**
 * @swagger
 * /metrics:
 *   get:
 *     summary: Expose Prometheus metrics
 *     description: Returns the current state of Prometheus metrics for the application.
 *     tags: [Monitoring]
 *     responses:
 *       200:
 *         description: Prometheus metrics formatted for scraping
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 */
router.get("/metrics", async (req, res) => {
  try {
    res.set("Content-Type", register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err);
  }
});

export default router;
