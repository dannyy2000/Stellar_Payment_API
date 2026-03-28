import express from "express";
import { merchantService } from "../services/merchantService.js";
import { requireApiKeyAuth } from "../lib/auth.js";

const router = express.Router();

/**
 * @swagger
 * /api/webhooks/logs:
 *   get:
 *     summary: Get webhook delivery logs for authenticated merchant
 *     description: Retrieve paginated webhook delivery logs for the authenticated merchant account
 *     tags: [Webhooks]
 *     security:
 *       - ApiKeyAuth: []
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
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                       payment_id:
 *                         type: string
 *                       status_code:
 *                         type: integer
 *                       success:
 *                         type: boolean
 *                       response_body:
 *                         type: string
 *                       timestamp:
 *                         type: string
 *                         format: date-time
 *                       payment:
 *                         type: object
 *                         properties:
 *                           amount:
 *                             type: number
 *                           asset:
 *                             type: string
 *                           status:
 *                             type: string
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
 *       401:
 *         description: Unauthorized - invalid or missing API key
 *       500:
 *         description: Server error
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
    
    const { data: logsData, error, count } = await query;
    
    if (error) {
      error.status = 500;
      throw error;
    }
    
    // Format response
    const logs = logsData.map(log => ({
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
 */
router.post("/webhooks/test", requireApiKeyAuth(), async (req, res, next) => {
  try {
    const result = await merchantService.testWebhook(req.merchant, req.merchant.webhook_url);
    
    if (!req.merchant.webhook_url) {
      return res.status(400).json({ error: "No webhook URL configured for this merchant." });
    }

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