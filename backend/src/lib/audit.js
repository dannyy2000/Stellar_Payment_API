/**
 * Audit Logging Helper
 *
 * Provides a lightweight helper to record merchant login attempts
 * (success and failure) into the `audit_logs` table for security monitoring.
 *
 * Design notes:
 * - All errors are swallowed so audit logging never blocks or crashes auth.
 * - `merchantId` is required (NOT NULL FK); only call this after merchant lookup.
 * - `status` is stored as a suffix of the `action` field: 'login_success' | 'login_failure'.
 */

import { pool } from "./db.js";

/**
 * Record a merchant login attempt in the audit_logs table.
 *
 * @param {object} opts
 * @param {string|null} opts.merchantId  - UUID of the merchant (null if unknown)
 * @param {string|null} opts.ipAddress   - Remote IP from req.ip
 * @param {string|null} opts.userAgent   - User-Agent header value
 * @param {'success'|'failure'} opts.status - Outcome of the login attempt
 * @returns {Promise<void>}
 */
export async function logLoginAttempt({ merchantId, ipAddress, userAgent, status }) {
  try {
    await pool.query(
      `INSERT INTO audit_logs (merchant_id, action, status, ip_address, user_agent)
       VALUES ($1, $2, $3, $4, $5)`,
      [merchantId ?? null, "login", status, ipAddress ?? null, userAgent ?? null],
    );
  } catch (err) {
    // Audit logging should never break the auth flow.
    console.error("Failed to write audit log:", err.message);
  }
}

