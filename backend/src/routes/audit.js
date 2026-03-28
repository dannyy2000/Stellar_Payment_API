/**
 * Audit Logs Routes
 * Issue #155: Merchant Profile Change Audit Logs
 */

import express from "express";
import { auditService } from "../services/auditService.js";
import { requireApiKeyAuth } from "../lib/auth.js";

const router = express.Router();

/**
 * @swagger
 * /api/audit-logs:
 *   get:
 *     summary: Get audit logs for the authenticated merchant
 *     tags: [Audit]
 *     security:
 *       - ApiKeyAuth: []
 */
router.get("/audit-logs", requireApiKeyAuth(), async (req, res, next) => {
  try {
    const { page, limit } = req.query;
    const result = await auditService.getAuditLogs(req.merchant.id, page, limit);
    res.json(result);
  } catch (err) {
    next(err);
  }
});

export default router;
