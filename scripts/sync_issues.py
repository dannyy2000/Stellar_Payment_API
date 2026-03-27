import subprocess
import json
import os
import time

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

# Define the 50 issues exactly as before
issues_metadata = [
    # (Copied data from create_v4_50_issues.py)
    {
        "title": "[BE] Implement SEP-0001 (stellar.toml) Generator",
        "labels": "backend,stellar,enhancement,complexity:medium,Stellar Wave",
        "body": """## Description\nImplement an automated `stellar.toml` generator that allows merchants to expose their business information according to the SEP-0001 standard.\n\n## Requirements and context\n- Create a route `GET /.well-known/stellar.toml`.\n- Dynamically generate content based on merchant settings in the database.\n- Support standard fields: `NETWORK_PASSPHRASE`, `FEDERATION_SERVER`, `TRANSFER_SERVER`, `ACCOUNTS`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/sep0001-generator`\n- **Implement changes:**\n  - Add `toml` parsing/generation library.\n  - Create the `.well-known` route in `backend/src/app.js`.\n- **Test and commit:**\n  - Verify the TOML output is valid using the Stellar Laboratory.\n\n## Example commit message\n`feat: implement SEP-0001 stellar.toml generator`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Asset Conversion: Implement Path Payments in Verification",
        "labels": "backend,stellar,enhancement,complexity:high,Stellar Wave",
        "body": """## Description\nAllow customers to pay in one asset (e.g., XLM) while the merchant receives another (e.g., USDC) via Stellar Path Payments.\n\n## Requirements and context\n- Update `findMatchingPayment` in `backend/src/lib/stellar.js` to handle `path_payment_strict_receive` operations.\n- Verify the received amount matches the intent after conversion.\n- Support path discovery for optimal conversion rates.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/path-payments`\n- **Implement changes:**\n  - Update StellarSDK logic to fetch path payments.\n  - Refactor verification logic to support cross-asset validation.\n- **Test and commit:**\n  - Simulate a path payment on Testnet and verify successful intent confirmation.\n\n## Example commit message\n`feat: support Stellar Path Payments in payment verification`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Data Retention: Automated DB Archival for Old Payment Intents",
        "labels": "backend,database,maintenance,complexity:medium,Stellar Wave",
        "body": """## Description\nImplement a job to archive payment intents older than 90 days to a cold storage table or external storage to maintain database performance.\n\n## Requirements and context\n- Create an `archived_payments` table.\n- Implement a cron-like behavior (e.g., via `node-cron` or `BullMQ`) to move old records.\n- Ensure referential integrity is preserved.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/payment-archival`\n- **Implement changes:**\n  - Use Knex to create archival migrations.\n  - Implement the archival script in `backend/src/lib/maintenance.js`.\n- **Test and commit:**\n  - Verify records are correctly moved and deleted from the main table.\n\n## Example commit message\n`feat: implement automated payment intent archival`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Security: Rate Limit Endpoint for Merchant Registration",
        "labels": "backend,security,bug,complexity:trivial,Stellar Wave",
        "body": """## Description\nProtect the merchant registration endpoint from brute-force attacks and spam.\n\n## Requirements and context\n- Apply a strict rate limit to `POST /api/merchants/register`.\n- Use the existing Redis-based rate limiter logic.\n- Return a clear `429 Too Many Requests` status code.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b fix/registration-rate-limit`\n- **Implement changes:**\n  - Add rate limit middleware to the registration route in `backend/src/routes/merchants.js`.\n- **Test and commit:**\n  - Verify that exceeding the limit blocks subsequent attempts.\n\n## Example commit message\n`fix: apply rate limiting to merchant registration endpoint`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Monitoring: Integration with Sentry for Backend Error Tracking",
        "labels": "backend,monitoring,dx,complexity:medium,Stellar Wave",
        "body": """## Description\nIntegrate Sentry into the backend to capture runtime exceptions and performance bottlenecks.\n\n## Requirements and context\n- Initialize Sentry in `backend/src/server.js`.\n- Add Sentry request/error handler middlewares.\n- Mask sensitive data (PII, secrets) in error reports.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/sentry-backend`\n- **Implement changes:**\n  - Install `@sentry/node`.\n  - Configure environment variables for Sentry DSN.\n- **Test and commit:**\n  - Trigger a test error and verify it appears in the Sentry dashboard.\n\n## Example commit message\n`feat: integrate Sentry for backend error tracking`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] API: Build Endpoint for Merchant Branding Customization",
        "labels": "backend,api,enhancement,complexity:medium,Stellar Wave",
        "body": """## Description\nAllow merchants to customize their payment link pages with their own logos and brand colors.\n\n## Requirements and context\n- Add `branding_config` (JSON) column to the `merchants` table.\n- Create `PUT /api/merchants/branding` endpoint.\n- Validate branding inputs (hex colors, URL formats) using Zod.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/merchant-branding`\n- **Implement changes:**\n  - Update merchant schema and router.\n  - Implement branding logic in `backend/src/lib/branding.js`.\n- **Test and commit:**\n  - Verify the branding configuration is correctly saved and retrieved.\n\n## Example commit message\n`feat: add merchant branding customization API`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Validation: Strict Type Check for Stellar Memos",
        "labels": "backend,bug,stellar,complexity:trivial,Stellar Wave",
        "body": """## Description\nEnsure that Stellar memos passed by merchants match the required format for their type (TEXT, ID, HASH, RETURN).\n\n## Requirements and context\n- Add validation logic in `backend/src/lib/stellar.js`.\n- Reject HASH/RETURN memos that aren'\''t 32-byte hex strings.\n- Return descriptive error messages for invalid memo formats.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b fix/memo-validation`\n- **Implement changes:**\n  - Update Zod schemas for payment intents.\n  - Add memo format checks before verification.\n- **Test and commit:**\n  - Verify invalid memos are rejected before reaching Horizon.\n\n## Example commit message\n`fix: implement strict validation for Stellar memo formats`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Scalability: Connection Pooling Optimization for PG",
        "labels": "backend,performance,database,complexity:medium,Stellar Wave",
        "body": """## Description\nOptimize the PostgreSQL connection pool settings to handle high concurrent traffic more efficiently.\n\n## Requirements and context\n- Tune `max`, `min`, `idleTimeoutMillis` in `backend/src/lib/db.js`.\n- Implement pool monitoring (e.g., logging pool usage statistics).\n- Ensure pool is shared correctly across the application.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b perf/db-pool-tuning`\n- **Implement changes:**\n  - Refactor DB pool initialization.\n- **Test and commit:**\n  - Use a load testing tool (e.g., `autocannon`) to verify performance improvements.\n\n## Example commit message\n`perf: optimize PostgreSQL connection pooling settings`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Audit: Log Merchant Login Attempts",
        "labels": "backend,security,audit,complexity:medium,Stellar Wave",
        "body": """## Description\nMaintain an audit trail of merchant login attempts (success and failure) for security monitoring.\n\n## Requirements and context\n- Create `audit_logs` table.\n- Capture: IP address, user agent, merchant ID, timestamp, and status.\n- Implement an audit logging helper in `backend/src/lib/audit.js`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/login-audit-logs`\n- **Implement changes:**\n  - Update authentication logic to record attempts.\n- **Test and commit:**\n  - Verify logs are correctly written on every login attempt.\n\n## Example commit message\n`feat: implement merchant login audit logging`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Integration: Implement Webhook Signature Header (HMAC-SHA256)",
        "labels": "backend,security,robustness,complexity:high,Stellar Wave",
        "body": """## Description\nSecure webhook deliveries by signing the payload with an HMAC-SHA256 signature using the merchant'\''s secret key.\n\n## Requirements and context\n- Add `Stellar-Signature` header to webhook requests.\n- Payloads should include a timestamp to prevent replay attacks.\n- Document how merchants should verify the signature.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/webhook-signing`\n- **Implement changes:**\n  - Add signature generation logic in `backend/src/lib/webhooks.js`.\n- **Test and commit:**\n  - Deliver a webhook and verify the signature using a test script.\n\n## Example commit message\n`feat: implement HMAC-SHA256 webhook signatures`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Testing: Build Integration Test Suite for Payment Lifecycle",
        "labels": "backend,testing,qa,complexity:high,Stellar Wave",
        "body": """## Description\nCreate a comprehensive integration test suite that covers the full lifecycle of a payment intent from creation to verification.\n\n## Requirements and context\n- Use `vitest` and `supertest`.\n- Mock Horizon responses using a library like `nock`.\n- Verify database state and webhook calls during the flow.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b test/payment-integration`\n- **Implement changes:**\n  - Create `backend/tests/integration/payments.test.js`.\n- **Test and commit:**\n  - Run the test suite and ensure it passes consistently.\n\n## Example commit message\n`test: add end-to-end integration tests for payment lifecycle`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Refactor: Extract Business Logic from Routes to Services",
        "labels": "backend,refactor,dx,complexity:medium,Stellar Wave",
        "body": """## Description\nRefactor the current router-heavy architecture by moving core business logic into dedicated service modules.\n\n## Requirements and context\n- Move payment logic to `services/paymentService.js`.\n- Move merchant logic to `services/merchantService.js`.\n- Improve code readability and testability.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b refactor/service-layer`\n- **Implement changes:**\n  - Refactor `backend/src/routes/payments.js` and `merchants.js`.\n- **Test and commit:**\n  - Ensure all existing tests pass after refactoring.\n\n## Example commit message\n`refactor: introduce service layer for business logic`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Documentation: Implement Automated API Docs with Swagger",
        "labels": "backend,dx,documentation,complexity:medium,Stellar Wave",
        "body": """## Description\nUse `swagger-jsdoc` to automatically generate OpenAPI documentation from JSDoc comments in route files.\n\n## Requirements and context\n- Configure Swagger UI in `backend/src/app.js`.\n- Annotate all existing endpoints.\n- Support API key authentication in the Swagger UI.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b docs/swagger-integration`\n- **Implement changes:**\n  - Update `backend/src/swagger.js`.\n- **Test and commit:**\n  - Access `/api-docs` and verify all endpoints are correctly documented.\n\n## Example commit message\n`docs: implement automated Swagger API documentation`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Robustness: Implement Request Validation Middleware",
        "labels": "backend,robustness,security,complexity:trivial,Stellar Wave",
        "body": """## Description\nCentralize request body and query parameter validation using Zod schemas to ensure consistency across the API.\n\n## Requirements and context\n- Create a `validateRequest` middleware.\n- Apply it to all data-entry routes.\n- Return detailed error messages when validation fails.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/request-validation`\n- **Implement changes:**\n  - Add middleware in `backend/src/lib/validation.js`.\n- **Test and commit:**\n  - Send malformed requests and verify they are rejected with proper error details.\n\n## Example commit message\n`feat: implement central request validation middleware`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Monitoring: Custom Prometheus Metrics for Payment Volume",
        "labels": "backend,monitoring,metrics,complexity:medium,Stellar Wave",
        "body": """## Description\nExpose custom Prometheus metrics to track payment volume, success rates, and latency.\n\n## Requirements and context\n- Use `prom-client`.\n- Define counters for `payment_created`, `payment_confirmed`, `payment_failed`.\n- Expose `/metrics` endpoint for collection.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b monitoring/prometheus-metrics`\n- **Implement changes:**\n  - Integrate metrics tracking in payment logic.\n- **Test and commit:**\n  - Verify metrics are correctly updated in the `/metrics` output.\n\n## Example commit message\n`feat: expose payment metrics for Prometheus monitoring`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Database: Multi-Index Optimization for Payments Table",
        "labels": "backend,database,performance,complexity:trivial,Stellar Wave",
        "body": """## Description\nImprove query performance for payment intents by adding composite indexes on frequently filtered columns.\n\n## Requirements and context\n- Add indexes on `(merchant_id, status)` and `(merchant_id, created_at)`.\n- Analyze query plans before and after.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b perf/payment-indexes`\n- **Implement changes:**\n  - Add migrations for new indexes.\n- **Test and commit:**\n  - Verify query performance improvements using `EXPLAIN ANALYZE`.\n\n## Example commit message\n`perf: add optimized indexes to payments table`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Security: Implement API Key Expiry and Rotation",
        "labels": "backend,security,api,complexity:high,Stellar Wave",
        "body": """## Description\nEnhance API security by adding support for expiring API keys and providing an automated rotation flow.\n\n## Requirements and context\n- Add `expires_at` column to merchant API keys.\n- Create rotation endpoint `POST /api/merchants/rotate-api-key`.\n- Ensure old keys remain valid for a brief overlap period.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/api-key-rotation`\n- **Implement changes:**\n  - Update merchant schema and auth middleware.\n- **Test and commit:**\n  - Verify key rotation and overlap behavior.\n\n## Example commit message\n`feat: implement API key expiry and rotation policy`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Asset Support: Add USDC (Ethereum/AssetHub) Issuers to Default List",
        "labels": "backend,stellar,config,complexity:trivial,Stellar Wave",
        "body": """## Description\nUpdate the default asset configuration to include known USDC issuers on the Stellar network.\n\n## Requirements and context\n- Add Centre USDC issuer addresses to the default configuration.\n- Update asset resolution logic to handle these issuers correctly.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b config/usdc-issuers`\n- **Implement changes:**\n  - Update `backend/src/lib/stellar.js` configuration.\n- **Test and commit:**\n  - Verify USDC payments are correctly recognized.\n\n## Example commit message\n`config: update default USDC asset issuers`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Robustness: Implement Global Error Handling Middleware",
        "labels": "backend,robustness,dx,complexity:trivial,Stellar Wave",
        "body": """## Description\nUnify error responses across the API by implementing a global error handling middleware.\n\n## Requirements and context\n- Catch all unhandled exceptions.\n- Sanitize error messages for production (no stack traces).\n- Return consistent JSON error objects.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b robustness/error-handler`\n- **Implement changes:**\n  - Add middleware to `backend/src/app.js`.\n- **Test and commit:**\n  - Trigger various error types and verify the output format.\n\n## Example commit message\n`feat: implement global error handling middleware`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Scaling: Implement Redis-based Idempotency Key Storage",
        "labels": "backend,scalability,robustness,complexity:high,Stellar Wave",
        "body": """## Description\nPrevent duplicate payment intents by implementing an idempotency key mechanism using Redis.\n\n## Requirements and context\n- Inspect `Idempotency-Key` header on create-payment requests.\n- Store results in Redis for a set duration (e.g., 24h).\n- Return cached results for duplicate keys.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/idempotency-keys`\n- **Implement changes:**\n  - Add idempotency middleware.\n- **Test and commit:**\n  - Verify that identical requests with the same key return the same result without double-creating.\n\n## Example commit message\n`feat: implement Redis-based request idempotency`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Integration: Add Support for Webhook Retries with Exponential Backoff",
        "labels": "backend,robustness,complexity:high,Stellar Wave",
        "body": """## Description\nImprove webhook reliability by implementing a retry mechanism with exponential backoff for failed deliveries.\n\n## Requirements and context\n- Use a worker/queue (e.g., `BullMQ`).\n- Track attempt count and status.\n- Max retries: 5 over 24 hours.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/webhook-retries`\n- **Implement changes:**\n  - Integrate a job queue.\n  - Refactor webhook delivery logic.\n- **Test and commit:**\n  - Mock delivery failures and verify retry intervals.\n\n## Example commit message\n`feat: implement robust webhook retry mechanism`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] API: Endpoint to Fetch Individual Payment Details (Extended)",
        "labels": "backend,api,enhancement,complexity:trivial,Stellar Wave",
        "body": """## Description\nProvide a detailed view of a payment intent, including the underlying Stellar transaction data if confirmed.\n\n## Requirements and context\n- Route: `GET /api/payments/:id`.\n- Include `tx_hash`, `ledger`, and `timestamp` if status is '\''completed'\''.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b api/payment-details`\n- **Implement changes:**\n  - Add route and logic.\n- **Test and commit:**\n  - Verify the returned JSON includes valid Stellar metadata.\n\n## Example commit message\n`feat: add detailed payment intent retrieval endpoint`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Security: Sanitize Metadata Payloads to Prevent XSS",
        "labels": "backend,security,bug,complexity:trivial,Stellar Wave",
        "body": """## Description\nSanitize the user-provided metadata field in payment intents to prevent potential XSS vulnerabilities when rendered in the dashboard.\n\n## Requirements and context\n- Use a library like `dompurify` or simple regex-based sanitization.\n- Apply to `metadata` field on creation.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b security/metadata-sanitization`\n- **Implement changes:**\n  - Add sanitization to payment services.\n- **Test and commit:**\n  - Verify malicious metadata is cleaned before storage.\n\n## Example commit message\n`fix: sanitize payment metadata to prevent XSS`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Database: Implement Soft Deletes for Merchants",
        "labels": "backend,database,feature,complexity:trivial,Stellar Wave",
        "body": """## Description\nAllow merchants to '\''delete'\'' their accounts while preserving their transaction history for audit purposes.\n\n## Requirements and context\n- Add `deleted_at` column to `merchants`.\n- Filter out deleted merchants from standard queries.\n- Block access for deleted merchant API keys.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/merchant-soft-delete`\n- **Implement changes:**\n  - Update schema and middlewares.\n- **Test and commit:**\n  - Verify the merchant is hidden and inaccessible after deletion.\n\n## Example commit message\n`feat: implement soft delete support for merchants`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] DX: Build Interactive CLI Tool for Testnet Simulation",
        "labels": "backend,dx,stellar,complexity:medium,Stellar Wave",
        "body": """## Description\nBuild a small internal CLI tool to help developers simulate payments on Testnet for local integration testing.\n\n## Requirements and context\n- Scripts to create keys, fund accounts via Friendbot, and send payments with specific memos.\n- Use `commander.js`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b tool/testnet-simulator`\n- **Implement changes:**\n  - Add script to `backend/scripts/simulate.js`.\n- **Test and commit:**\n  - Use the tool to successfully confirm a local payment intent.\n\n## Example commit message\n`feat: add CLI tool for Stellar testnet payment simulation`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Dashboard: Move Dashboard Home to dedicated /dashboard route",
        "labels": "frontend,refactor,ux,complexity:medium,Stellar Wave",
        "body": """## Description\nSeparate the public landing page from the authenticated dashboard management area.\n\n## Requirements and context\n- Move the current `/` logic to `/dashboard`.\n- Build a new landing page (marketing focus) at `/`.\n- Implement redirects for authenticated users.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b refactor/dashboard-routes`\n- **Implement changes:**\n  - Update Next.js page structure.\n  - Implement middleware-based redirection.\n- **Test and commit:**\n  - Verify that `/dashboard` requires login and `/` is accessible to everyone.\n\n## Example commit message\n`refactor: separate marketing home from merchant dashboard`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Payment Logic: Implement Real-time Polking-based Feedback on Checkout",
        "labels": "frontend,ux,stellar,complexity:medium,Stellar Wave",
        "body": """## Description\nProvide immediate feedback to the customer on the checkout page when their payment is detected and confirmed on-chain.\n\n## Requirements and context\n- Polling `GET /api/payments/:id` every 3 seconds while on checkout.\n- Transition from '\''Waiting for Payment'\'' to '\''Success'\'' state automatically.\n- Show transaction confetti on success.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/checkout-realtime-status`\n- **Implement changes:**\n  - Update `frontend/src/app/(public)/pay/[id]/page.tsx`.\n- **Test and commit:**\n  - Perform a payment and verify the UI updates without manual refresh.\n\n## Example commit message\n`feat: implement real-time payment status updates in checkout UI`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] UI Library: Build Skeleton Loading for Metrics Cards",
        "labels": "frontend,ux,design,complexity:trivial,Stellar Wave",
        "body": """## Description\nImprove the perceived performance of the dashboard by showing skeleton loaders while metrics data is being fetched.\n\n## Requirements and context\n- Use `react-loading-skeleton`.\n- Match the layout of `PaymentMetrics.tsx`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/metrics-skeletons`\n- **Implement changes:**\n  - Create `MetricsSkeleton.tsx`.\n  - Update the metrics container to show skeletons during loading states.\n- **Test and commit:**\n  - Slow down the network and verify the skeletons render correctly.\n\n## Example commit message\n`ui: add skeleton loading states to dashboard metrics`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Settings: API Key Copy To Clipboard with UI Feedback",
        "labels": "frontend,ux,complexity:trivial,Stellar Wave",
        "body": """## Description\nMake it easier for developers to manage their API keys by adding a reliable '\''copy to clipboard'\'' button with visual success feedback.\n\n## Requirements and context\n- Use `navigator.clipboard`.\n- Show a success toast or icon change on copy.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/copy-api-key`\n- **Implement changes:**\n  - Update `ApiKeysPage.tsx`.\n- **Test and commit:**\n  - Verify the key is correctly copied to the clipboard.\n\n## Example commit message\n`ui: add copy-to-clipboard button with feedback for API keys`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Checkout: Localize Checkout Page to Spanish (ES) and Portuguese (PT)",
        "labels": "frontend,i18n,complexity:medium,Stellar Wave",
        "body": """## Description\nExpand the reach of our payment links by localizing the checkout experience for the LATAM market.\n\n## Requirements and context\n- Use `next-intl` or similar.\n- Translate: '\''Total Amount'\'', '\''Asset'\'', '\''Waiting for Payment'\'', '\''Confirming'\'', '\''Payment Successful'\''.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b i18n/latam-checkout`\n- **Implement changes:**\n  - Add translation JSONs.\n  - Wrap checkout components in i18n providers.\n- **Test and commit:**\n  - Verify translations load based on browser language or selector.\n\n## Example commit message\n`feat: localize checkout UI for Spanish and Portuguese`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Branding: Dynamic Checkout Colors based on Merchant Config",
        "labels": "frontend,design,ux,complexity:medium,Stellar Wave",
        "body": """## Description\nApply merchant-specific branding (primary colors and logos) to the public checkout page.\n\n## Requirements and context\n- Fetch branding config from the backend.\n- Use CSS variables to inject custom colors into Tailwind theme.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/dynamic-checkout-branding`\n- **Implement changes:**\n  - Update `frontend/src/app/(public)/pay/[id]/page.tsx` to handle branding data.\n- **Test and commit:**\n  - Change branding in the database and verify the checkout page reflects changes.\n\n## Example commit message\n`feat: implement dynamic merchant branding for checkout pages`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Dashboard: Add Search and Pagination to Payment Table",
        "labels": "frontend,api,ux,complexity:high,Stellar Wave",
        "body": """## Description\nImprove manageability of large datasets by adding server-side search and pagination to the payments list.\n\n## Requirements and context\n- Search by `recipient` or `amount`.\n- Implement page buttons and '\''items per page'\'' selector.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/paginated-payment-table`\n- **Implement changes:**\n  - Update backend endpoints to support `?page=&limit=&q=`.\n  - Refactor frontend table to use query parameters.\n- **Test and commit:**\n  - Verify search results and page transitions are smooth.\n\n## Example commit message\n`feat: add server-side search and pagination to payments dashboard`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] UI: Implement Animated Success State for Payment Creation",
        "labels": "frontend,design,ux,complexity:trivial,Stellar Wave",
        "body": """## Description\nMake the payment link generation feel more premium with a smooth success transition and confetti effect.\n\n## Requirements and context\n- Use `framer-motion` for transitions.\n- Integrate `canvas-confetti`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/payment-creation-feedback`\n- **Implement changes:**\n  - Update `CreatePaymentForm.tsx`.\n- **Test and commit:**\n  - Create an intent and verify the animation sequence.\n\n## Example commit message\n`ui: add animated success state for payment link generation`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Desktop: Global Dashboard Sidebar Component",
        "labels": "frontend,ux,design,complexity:medium,Stellar Wave",
        "body": """## Description\nEstablish a consistent navigation structure for authenticated users using a sidebar rather than only a top navigation bar.\n\n## Requirements and context\n- Icons for: Overview, Payments, Webhook Logs, Settings.\n- Responsive behavior: Collapsible on desktop, drawer on mobile.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/dashboard-sidebar`\n- **Implement changes:**\n  - Create `src/components/Sidebar.tsx`.\n- **Test and commit:**\n  - Verify smooth navigation across all dashboard sub-pages.\n\n## Example commit message\n`ui: implement persistent dashboard navigation sidebar`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Checkout: Show Stellar.expert Link after Confirmation",
        "labels": "frontend,stellar,dx,complexity:trivial,Stellar Wave",
        "body": """## Description\nProvide transparency to customers by linking to the transaction on the block explorer once confirmed.\n\n## Requirements and context\n- Use `stellar.expert` as the default explorer.\n- Open link in a new tab.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/explorer-link`\n- **Implement changes:**\n  - Update the success view in the checkout page.\n- **Test and commit:**\n  - Click the link after a successful payment and verify it opens the correct transaction ID.\n\n## Example commit message\n`feat: add block explorer links to checkout success view`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Monitoring: Front-end Session Recording with Sentry Replay",
        "labels": "frontend,monitoring,ux,complexity:medium,Stellar Wave",
        "body": """## Description\nIntegrate Sentry Session Replay to debug user frustrations and UI crashes in real-time.\n\n## Requirements and context\n- Replay: Catch user clicks, scrolls, and errors.\n- Mask PII automatically.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/sentry-replay`\n- **Implement changes:**\n  - Update Sentry configuration in `sentry.client.config.ts`.\n- **Test and commit:**\n  - Verify replays are being captured in the Sentry Dashboard.\n\n## Example commit message\n`feat: enable Sentry Session Replay for frontend monitoring`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Documentation: Migration to MDX for Static Docs",
        "labels": "frontend,dx,documentation,complexity:high,Stellar Wave",
        "body": """## Description\nTransform the documentation area into a powerful developer portal using MDX to allow interactive code examples.\n\n## Requirements and context\n- Use `next-mdx-remote` or similar.\n- Implement a documentation layout with a nested sidebar.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b docs/mdx-migration`\n- **Implement changes:**\n  - Convert markdown files to `.mdx`.\n  - Add syntax highlighting support (`rehype-prism-plus`).\n- **Test and commit:**\n  - Verify docs render correctly and code blocks are highlighted.\n\n## Example commit message\n`docs: migrate documentation to MDX with syntax highlighting`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Performance: Multi-Region Edge Caching for Asset Metadata",
        "labels": "frontend,performance,complexity:high,Stellar Wave",
        "body": """## Description\nOptimize the loading of common asset metadata (XLM/USDC logos and names) using Next.js Incremental Static Regeneration (ISR).\n\n## Requirements and context\n- Cache asset data at the edge for 1 hour.\n- Reduce re-validation calls to Horizon.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b perf/asset-metadata-cache`\n- **Implement changes:**\n  - Implement ISR in dashboard components fetching asset info.\n- **Test and commit:**\n  - Measure first-page load speed with and without caching.\n\n## Example commit message\n`perf: implement ISR for asset metadata edge caching`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Mobile: Responsive Bottom Navigation for PWA support",
        "labels": "frontend,mobile,ux,complexity:medium,Stellar Wave",
        "body": """## Description\nEnhance the mobile experience by adding a standard bottom navigation bar when viewed on small screens.\n\n## Requirements and context\n- Hide sidebar on mobile.\n- Bottom bar icons: Home, Payments, Create, Settings.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/mobile-bottom-nav`\n- **Implement changes:**\n  - Create `src/components/MobileNav.tsx`.\n- **Test and commit:**\n  - Use Chrome DevTools mobile view and verify accessibility and touch target size.\n\n## Example commit message\n`ui: add responsive bottom navigation for mobile users`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Testing: Build Comprehensive E2E Test Suite for Checkout",
        "labels": "frontend,testing,qa,complexity:high,Stellar Wave",
        "body": """## Description\nImplement a Playwright test suite to ensure the critical checkout path never breaks.\n\n## Requirements and context\n- Tests: Rendering, QR code visibility, Wallet select modal, Error handling.\n- Run on multiple browsers (Chromium, Firefox, Webkit).\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b test/playback-checkout-e2e`\n- **Implement changes:**\n  - Create `tests/checkout.spec.ts`.\n- **Test and commit:**\n  - Run the tests locally and in CI to verify stability.\n\n## Example commit message\n`test: implement E2E checkouts suite with Playwright`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Add '\''Pay with QR code'\'' Modal with Download button",
        "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave",
        "body": """## Description\nAllow users to easily download the payment QR code to scan it on another device or share it via chat.\n\n## Requirements and context\n- Add a download icon to the QR component.\n- Support PNG export.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/qr-download`\n- **Implement changes:**\n  - Add download logic using a canvas referer.\n- **Test and commit:**\n  - Verify the downloaded image is clear and can be scanned.\n\n## Example commit message\n`feat: add QR code download functionality to checkout`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Dashboard: Charting - Add Weekly Average Volume",
        "labels": "frontend,analytics,ux,complexity:medium,Stellar Wave",
        "body": """## Description\nHelp merchants identify trends by showing a weekly rolling average on their volume charts.\n\n## Requirements and context\n- Use `recharts` to add a secondary trend line.\n- Calculate moving average in the dashboard hooks.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b analytics/weekly-average`\n- **Implement changes:**\n  - Update `PaymentMetrics.tsx`.\n- **Test and commit:**\n  - Verify the trend line calculation matches the raw data points.\n\n## Example commit message\n`feat: add weekly average trend line to metrics chart`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Accessability: Pass WCAG 2.1 Contrast Guidelines for Dashboard",
        "labels": "frontend,accessibility,bug,complexity:medium,Stellar Wave",
        "body": """## Description\nAudit and fix accessibility issues across the dashboard to ensure compliance with WCAG 2.1 standards.\n\n## Requirements and context\n- Fix contrast ratios for muted text.\n- Ensure all interactive elements have correct `aria-label` attributes.\n- Keyboard navigation check.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b accessibility/dashboard-audit`\n- **Implement changes:**\n  - Audit using Lighthouse or axe-core.\n  - Apply color and ARIA fixes.\n- **Test and commit:**\n  - Verify Lighthouse accessibility score is 100.\n\n## Example commit message\n`fix: improve dashboard accessibility to meet WCAG 2.1 compliance`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Settings: Merchant Domain Verification for Webhooks",
        "labels": "frontend,security,feature,complexity:high,Stellar Wave",
        "body": """## Description\nImplement a domain verification flow for webhooks to ensure that merchants actually control the endpoints they are configuring.\n\n## Requirements and context\n- File-based verification (`/.well-known/stellar-pay-verification.txt`).\n- Dashboard UI showing '\''Verified'\'' or '\''Unverified'\'' status.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/domain-verification`\n- **Implement changes:**\n  - Add verification logic to backend and frontend settings UI.\n- **Test and commit:**\n  - Verify that a domain is only marked as verified if the token matches.\n\n## Example commit message\n`feat: implement domain verification for merchant webhooks`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Show Stellar Fee Breakdown in Modal",
        "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave",
        "body": """## Description\nProvide transparency to the user by showing the estimated network fees (stroops) for their transaction before they pay.\n\n## Requirements and context\n- Fetch current Testnet/Mainnet fee stats.\n- Show '\''Network Fee: ~0.00001 XLM'\'' in the checkout modal.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/fee-transparency`\n- **Implement changes:**\n  - Use `server.feeStats()` from StellarSDK.\n- **Test and commit:**\n  - Verify the fee updates in response to network demand.\n\n## Example commit message\n`ui: show transparent Stellar network fee estimate on checkout`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Dashboard: Add Multi-Select for Bulk Webhook Retries",
        "labels": "frontend,ux,api,complexity:medium,Stellar Wave",
        "body": """## Description\nSave merchant time by allowing them to select multiple failed webhooks from the logs and retry them all in one click.\n\n## Requirements and context\n- Add checkboxes to the Webhook Logs table.\n- Implement `POST /api/webhooks/retry-bulk`.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/bulk-webhook-retry`\n- **Implement changes:**\n  - Update table UI and add bulk retry action.\n- **Test and commit:**\n  - Verify that all selected logs are correctly queued for retry.\n\n## Example commit message\n`feat: add bulk retry functionality to webhook logs`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] UI: Implement Copy-Button with '\''Glitch'\'' Animation on Success",
        "labels": "frontend,design,ux,complexity:trivial,Stellar Wave",
        "body": """## Description\nAdd a unique, on-brand '\''glitch'\'' animation to the copy button when a copy is successful, matching our premium dark/hacker aesthetic.\n\n## Requirements and context\n- Use `framer-motion` keyframes.\n- Apply to `CopyButton` component.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/glitch-copy-feedback`\n- **Implement changes:**\n  - Add animation variants to the button.\n- **Test and commit:**\n  - Copy an item and verify the visual effect.\n\n## Example commit message\n`ui: add premium glitch animation to copy button feedback`\n\n## Guidelines\n- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Branding: Support for Light Theme (Experimental Toggle)",
        "labels": "frontend,design,feature,complexity:high,Stellar Wave",
        "body": """## Description\nImplement an experimental light theme toggle for merchants who prefer light mode, ensuring accessibility and flexibility.\n\n## Requirements and context\n- Use CSS Variables or Tailwind dark: prefix.\n- Store preference in localStorage.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b ui/light-mode-support`\n- **Implement changes:**\n  - Add theme toggle to header.\n  - Define light-mode color palette.\n- **Test and commit:**\n  - Toggle themes and verify no unreadable text exists in either mode.\n\n## Example commit message\n`feat: implement experimental light theme support`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Show '\''Pay in XLM'\'' even if Invoice is USDC (using path payments)",
        "labels": "frontend,stellar,ux,complexity:high,Stellar Wave",
        "body": """## Description\nIncrease conversion by allowing users to pay with their native XLM even if the merchant expects USDC, leveraging Stellar Path Payments under the hood.\n\n## Requirements and context\n- Detect optimal paths for conversion.\n- Show '\''Approximate cost in XLM'\'' at checkout.\n- Execute path payment via Freighter/WalletConnect.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b feature/checkout-path-payment`\n- **Implement changes:**\n  - Integrate path discovery in the checkout page.\n- **Test and commit:**\n  - Complete an XLM->USDC payment flow successfully.\n\n## Example commit message\n`feat: support paying in XLM for USDC invoices via path payments`\n\n## Guidelines\n- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Testing: Add Visual Regression Tests with Playwright",
        "labels": "frontend,testing,qa,complexity:medium,Stellar Wave",
        "body": """## Description\nSet up basic visual regression testing for critical components to ensure that UI changes don'\''t cause unexpected regressions.\n\n## Requirements and context\n- Use `playwright` visual comparison.\n- Capture: Dashboard Home, Checkout, Settings.\n\n## Suggested execution\n- **Fork the repo and create a branch:** `git checkout -b test/visual-regression`\n- **Implement changes:**\n  - Add visual test scripts.\n- **Test and commit:**\n  - Verify a deliberate change triggers a test failure.\n\n## Example commit message\n`test: add visual regression testing for critical dashboard paths`\n\n## Guidelines\n- Complexity: Medium (150 points)"""
    }
]

print("Fetching latest issues...")
cmd_list = [gh_path, "issue", "list", "--repo", repo, "--limit", "300", "--state", "all", "--json", "number,title"]
result = subprocess.run(cmd_list, capture_output=True, text=True)
issues_on_gh = json.loads(result.stdout)

print(f"Syncing {len(issues_metadata)} issues (Create if missing, update labels if exists)...")
for issue_data in issues_metadata:
    # Find the issue number by title
    match = next((i for i in issues_on_gh if i["title"] == issue_data["title"]), None)
    
    if match:
        number = match["number"]
        labels = [l.strip() for l in issue_data["labels"].split(",")]
        
        print(f"Syncing labels for Issue #{number}: {issue_data['title']}")
        cmd_edit = [gh_path, "issue", "edit", str(number), "--repo", repo]
        for label in labels:
            cmd_edit.extend(["--add-label", label])
        
        subprocess.run(cmd_edit, capture_output=True)
    else:
        print(f"Issue missing, creating: {issue_data['title']}")
        cmd_create = [
            gh_path, "issue", "create", 
            "--repo", repo, 
            "--title", issue_data["title"], 
            "--body", issue_data["body"]
        ]
        # Handle labels
        labels = [l.strip() for l in issue_data["labels"].split(",")]
        for label in labels:
            cmd_create.extend(["--label", label])
        
        subprocess.run(cmd_create, capture_output=True)
        time.sleep(1.5)

print("All issues synced successfully!")
