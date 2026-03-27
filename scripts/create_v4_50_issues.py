import subprocess
import time
import os

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

# ────────────── 50 NEW ISSUES (Numbers 273-322) ──────────────
# 25 Backend, 25 Frontend

issues = [
    # --- BACKEND (25) ---
    {
        "title": "[BE] Implement SEP-0001 (stellar.toml) Generator",
        "labels": "backend,stellar,enhancement,complexity:medium,Stellar Wave",
        "body": """## Description
Implement an automated `stellar.toml` generator that allows merchants to expose their business information according to the SEP-0001 standard.

## Requirements and context
- Create a route `GET /.well-known/stellar.toml`.
- Dynamically generate content based on merchant settings in the database.
- Support standard fields: `NETWORK_PASSPHRASE`, `FEDERATION_SERVER`, `TRANSFER_SERVER`, `ACCOUNTS`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/sep0001-generator`
- **Implement changes:**
  - Add `toml` parsing/generation library.
  - Create the `.well-known` route in `backend/src/app.js`.
- **Test and commit:**
  - Verify the TOML output is valid using the Stellar Laboratory.

## Example commit message
`feat: implement SEP-0001 stellar.toml generator`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Asset Conversion: Implement Path Payments in Verification",
        "labels": "backend,stellar,enhancement,complexity:high,Stellar Wave",
        "body": """## Description
Allow customers to pay in one asset (e.g., XLM) while the merchant receives another (e.g., USDC) via Stellar Path Payments.

## Requirements and context
- Update `findMatchingPayment` in `backend/src/lib/stellar.js` to handle `path_payment_strict_receive` operations.
- Verify the received amount matches the intent after conversion.
- Support path discovery for optimal conversion rates.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/path-payments`
- **Implement changes:**
  - Update StellarSDK logic to fetch path payments.
  - Refactor verification logic to support cross-asset validation.
- **Test and commit:**
  - Simulate a path payment on Testnet and verify successful intent confirmation.

## Example commit message
`feat: support Stellar Path Payments in payment verification`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Data Retention: Automated DB Archival for Old Payment Intents",
        "labels": "backend,database,maintenance,complexity:medium,Stellar Wave",
        "body": """## Description
Implement a job to archive payment intents older than 90 days to a cold storage table or external storage to maintain database performance.

## Requirements and context
- Create an `archived_payments` table.
- Implement a cron-like behavior (e.g., via `node-cron` or `BullMQ`) to move old records.
- Ensure referential integrity is preserved.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/payment-archival`
- **Implement changes:**
  - Use Knex to create archival migrations.
  - Implement the archival script in `backend/src/lib/maintenance.js`.
- **Test and commit:**
  - Verify records are correctly moved and deleted from the main table.

## Example commit message
`feat: implement automated payment intent archival`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Security: Rate Limit Endpoint for Merchant Registration",
        "labels": "backend,security,bug,complexity:trivial,Stellar Wave",
        "body": """## Description
Protect the merchant registration endpoint from brute-force attacks and spam.

## Requirements and context
- Apply a strict rate limit to `POST /api/merchants/register`.
- Use the existing Redis-based rate limiter logic.
- Return a clear `429 Too Many Requests` status code.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/registration-rate-limit`
- **Implement changes:**
  - Add rate limit middleware to the registration route in `backend/src/routes/merchants.js`.
- **Test and commit:**
  - Verify that exceeding the limit blocks subsequent attempts.

## Example commit message
`fix: apply rate limiting to merchant registration endpoint`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Monitoring: Integration with Sentry for Backend Error Tracking",
        "labels": "backend,monitoring,dx,complexity:medium,Stellar Wave",
        "body": """## Description
Integrate Sentry into the backend to capture runtime exceptions and performance bottlenecks.

## Requirements and context
- Initialize Sentry in `backend/src/server.js`.
- Add Sentry request/error handler middlewares.
- Mask sensitive data (PII, secrets) in error reports.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/sentry-backend`
- **Implement changes:**
  - Install `@sentry/node`.
  - Configure environment variables for Sentry DSN.
- **Test and commit:**
  - Trigger a test error and verify it appears in the Sentry dashboard.

## Example commit message
`feat: integrate Sentry for backend error tracking`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] API: Build Endpoint for Merchant Branding Customization",
        "labels": "backend,api,enhancement,complexity:medium,Stellar Wave",
        "body": """## Description
Allow merchants to customize their payment link pages with their own logos and brand colors.

## Requirements and context
- Add `branding_config` (JSON) column to the `merchants` table.
- Create `PUT /api/merchants/branding` endpoint.
- Validate branding inputs (hex colors, URL formats) using Zod.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/merchant-branding`
- **Implement changes:**
  - Update merchant schema and router.
  - Implement branding logic in `backend/src/lib/branding.js`.
- **Test and commit:**
  - Verify the branding configuration is correctly saved and retrieved.

## Example commit message
`feat: add merchant branding customization API`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Validation: Strict Type Check for Stellar Memos",
        "labels": "backend,bug,stellar,complexity:trivial,Stellar Wave",
        "body": """## Description
Ensure that Stellar memos passed by merchants match the required format for their type (TEXT, ID, HASH, RETURN).

## Requirements and context
- Add validation logic in `backend/src/lib/stellar.js`.
- Reject HASH/RETURN memos that aren't 32-byte hex strings.
- Return descriptive error messages for invalid memo formats.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/memo-validation`
- **Implement changes:**
  - Update Zod schemas for payment intents.
  - Add memo format checks before verification.
- **Test and commit:**
  - Verify invalid memos are rejected before reaching Horizon.

## Example commit message
`fix: implement strict validation for Stellar memo formats`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Scalability: Connection Pooling Optimization for PG",
        "labels": "backend,performance,database,complexity:medium,Stellar Wave",
        "body": """## Description
Optimize the PostgreSQL connection pool settings to handle high concurrent traffic more efficiently.

## Requirements and context
- Tune `max`, `min`, `idleTimeoutMillis` in `backend/src/lib/db.js`.
- Implement pool monitoring (e.g., logging pool usage statistics).
- Ensure pool is shared correctly across the application.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b perf/db-pool-tuning`
- **Implement changes:**
  - Refactor DB pool initialization.
- **Test and commit:**
  - Use a load testing tool (e.g., `autocannon`) to verify performance improvements.

## Example commit message
`perf: optimize PostgreSQL connection pooling settings`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Audit: Log Merchant Login Attempts",
        "labels": "backend,security,audit,complexity:medium,Stellar Wave",
        "body": """## Description
Maintain an audit trail of merchant login attempts (success and failure) for security monitoring.

## Requirements and context
- Create `audit_logs` table.
- Capture: IP address, user agent, merchant ID, timestamp, and status.
- Implement an audit logging helper in `backend/src/lib/audit.js`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/login-audit-logs`
- **Implement changes:**
  - Update authentication logic to record attempts.
- **Test and commit:**
  - Verify logs are correctly written on every login attempt.

## Example commit message
`feat: implement merchant login audit logging`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Integration: Implement Webhook Signature Header (HMAC-SHA256)",
        "labels": "backend,security,robustness,complexity:high,Stellar Wave",
        "body": """## Description
Secure webhook deliveries by signing the payload with an HMAC-SHA256 signature using the merchant's secret key.

## Requirements and context
- Add `Stellar-Signature` header to webhook requests.
- Payloads should include a timestamp to prevent replay attacks.
- Document how merchants should verify the signature.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/webhook-signing`
- **Implement changes:**
  - Add signature generation logic in `backend/src/lib/webhooks.js`.
- **Test and commit:**
  - Deliver a webhook and verify the signature using a test script.

## Example commit message
`feat: implement HMAC-SHA256 webhook signatures`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Testing: Build Integration Test Suite for Payment Lifecycle",
        "labels": "backend,testing,qa,complexity:high,Stellar Wave",
        "body": """## Description
Create a comprehensive integration test suite that covers the full lifecycle of a payment intent from creation to verification.

## Requirements and context
- Use `vitest` and `supertest`.
- Mock Horizon responses using a library like `nock`.
- Verify database state and webhook calls during the flow.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b test/payment-integration`
- **Implement changes:**
  - Create `backend/tests/integration/payments.test.js`.
- **Test and commit:**
  - Run the test suite and ensure it passes consistently.

## Example commit message
`test: add end-to-end integration tests for payment lifecycle`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Refactor: Extract Business Logic from Routes to Services",
        "labels": "backend,refactor,dx,complexity:medium,Stellar Wave",
        "body": """## Description
Refactor the current router-heavy architecture by moving core business logic into dedicated service modules.

## Requirements and context
- Move payment logic to `services/paymentService.js`.
- Move merchant logic to `services/merchantService.js`.
- Improve code readability and testability.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b refactor/service-layer`
- **Implement changes:**
  - Refactor `backend/src/routes/payments.js` and `merchants.js`.
- **Test and commit:**
  - Ensure all existing tests pass after refactoring.

## Example commit message
`refactor: introduce service layer for business logic`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Documentation: Implement Automated API Docs with Swagger",
        "labels": "backend,dx,documentation,complexity:medium,Stellar Wave",
        "body": """## Description
Use `swagger-jsdoc` to automatically generate OpenAPI documentation from JSDoc comments in route files.

## Requirements and context
- Configure Swagger UI in `backend/src/app.js`.
- Annotate all existing endpoints.
- Support API key authentication in the Swagger UI.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b docs/swagger-integration`
- **Implement changes:**
  - Update `backend/src/swagger.js`.
- **Test and commit:**
  - Access `/api-docs` and verify all endpoints are correctly documented.

## Example commit message
`docs: implement automated Swagger API documentation`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Robustness: Implement Request Validation Middleware",
        "labels": "backend,robustness,security,complexity:trivial,Stellar Wave",
        "body": """## Description
Centralize request body and query parameter validation using Zod schemas to ensure consistency across the API.

## Requirements and context
- Create a `validateRequest` middleware.
- Apply it to all data-entry routes.
- Return detailed error messages when validation fails.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/request-validation`
- **Implement changes:**
  - Add middleware in `backend/src/lib/validation.js`.
- **Test and commit:**
  - Send malformed requests and verify they are rejected with proper error details.

## Example commit message
`feat: implement central request validation middleware`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Monitoring: Custom Prometheus Metrics for Payment Volume",
        "labels": "backend,monitoring,metrics,complexity:medium,Stellar Wave",
        "body": """## Description
Expose custom Prometheus metrics to track payment volume, success rates, and latency.

## Requirements and context
- Use `prom-client`.
- Define counters for `payment_created`, `payment_confirmed`, `payment_failed`.
- Expose `/metrics` endpoint for collection.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b monitoring/prometheus-metrics`
- **Implement changes:**
  - Integrate metrics tracking in payment logic.
- **Test and commit:**
  - Verify metrics are correctly updated in the `/metrics` output.

## Example commit message
`feat: expose payment metrics for Prometheus monitoring`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[BE] Database: Multi-Index Optimization for Payments Table",
        "labels": "backend,database,performance,complexity:trivial,Stellar Wave",
        "body": """## Description
Improve query performance for payment intents by adding composite indexes on frequently filtered columns.

## Requirements and context
- Add indexes on `(merchant_id, status)` and `(merchant_id, created_at)`.
- Analyze query plans before and after.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b perf/payment-indexes`
- **Implement changes:**
  - Add migrations for new indexes.
- **Test and commit:**
  - Verify query performance improvements using `EXPLAIN ANALYZE`.

## Example commit message
`perf: add optimized indexes to payments table`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Security: Implement API Key Expiry and Rotation",
        "labels": "backend,security,api,complexity:high,Stellar Wave",
        "body": """## Description
Enhance API security by adding support for expiring API keys and providing an automated rotation flow.

## Requirements and context
- Add `expires_at` column to merchant API keys.
- Create rotation endpoint `POST /api/merchants/rotate-api-key`.
- Ensure old keys remain valid for a brief overlap period.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/api-key-rotation`
- **Implement changes:**
  - Update merchant schema and auth middleware.
- **Test and commit:**
  - Verify key rotation and overlap behavior.

## Example commit message
`feat: implement API key expiry and rotation policy`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Asset Support: Add USDC (Ethereum/AssetHub) Issuers to Default List",
        "labels": "backend,stellar,config,complexity:trivial,Stellar Wave",
        "body": """## Description
Update the default asset configuration to include known USDC issuers on the Stellar network.

## Requirements and context
- Add Centre USDC issuer addresses to the default configuration.
- Update asset resolution logic to handle these issuers correctly.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b config/usdc-issuers`
- **Implement changes:**
  - Update `backend/src/lib/stellar.js` configuration.
- **Test and commit:**
  - Verify USDC payments are correctly recognized.

## Example commit message
`config: update default USDC asset issuers`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Robustness: Implement Global Error Handling Middleware",
        "labels": "backend,robustness,dx,complexity:trivial,Stellar Wave",
        "body": """## Description
Unify error responses across the API by implementing a global error handling middleware.

## Requirements and context
- Catch all unhandled exceptions.
- Sanitize error messages for production (no stack traces).
- Return consistent JSON error objects.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b robustness/error-handler`
- **Implement changes:**
  - Add middleware to `backend/src/app.js`.
- **Test and commit:**
  - Trigger various error types and verify the output format.

## Example commit message
`feat: implement global error handling middleware`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Scaling: Implement Redis-based Idempotency Key Storage",
        "labels": "backend,scalability,robustness,complexity:high,Stellar Wave",
        "body": """## Description
Prevent duplicate payment intents by implementing an idempotency key mechanism using Redis.

## Requirements and context
- Inspect `Idempotency-Key` header on create-payment requests.
- Store results in Redis for a set duration (e.g., 24h).
- Return cached results for duplicate keys.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/idempotency-keys`
- **Implement changes:**
  - Add idempotency middleware.
- **Test and commit:**
  - Verify that identical requests with the same key return the same result without double-creating.

## Example commit message
`feat: implement Redis-based request idempotency`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] Integration: Add Support for Webhook Retries with Exponential Backoff",
        "labels": "backend,robustness,complexity:high,Stellar Wave",
        "body": """## Description
Improve webhook reliability by implementing a retry mechanism with exponential backoff for failed deliveries.

## Requirements and context
- Use a worker/queue (e.g., `BullMQ`).
- Track attempt count and status.
- Max retries: 5 over 24 hours.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/webhook-retries`
- **Implement changes:**
  - Integrate a job queue.
  - Refactor webhook delivery logic.
- **Test and commit:**
  - Mock delivery failures and verify retry intervals.

## Example commit message
`feat: implement robust webhook retry mechanism`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[BE] API: Endpoint to Fetch Individual Payment Details (Extended)",
        "labels": "backend,api,enhancement,complexity:trivial,Stellar Wave",
        "body": """## Description
Provide a detailed view of a payment intent, including the underlying Stellar transaction data if confirmed.

## Requirements and context
- Route: `GET /api/payments/:id`.
- Include `tx_hash`, `ledger`, and `timestamp` if status is 'completed'.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b api/payment-details`
- **Implement changes:**
  - Add route and logic.
- **Test and commit:**
  - Verify the returned JSON includes valid Stellar metadata.

## Example commit message
`feat: add detailed payment intent retrieval endpoint`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Security: Sanitize Metadata Payloads to Prevent XSS",
        "labels": "backend,security,bug,complexity:trivial,Stellar Wave",
        "body": """## Description
Sanitize the user-provided metadata field in payment intents to prevent potential XSS vulnerabilities when rendered in the dashboard.

## Requirements and context
- Use a library like `dompurify` or simple regex-based sanitization.
- Apply to `metadata` field on creation.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b security/metadata-sanitization`
- **Implement changes:**
  - Add sanitization to payment services.
- **Test and commit:**
  - Verify malicious metadata is cleaned before storage.

## Example commit message
`fix: sanitize payment metadata to prevent XSS`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Database: Implement Soft Deletes for Merchants",
        "labels": "backend,database,feature,complexity:trivial,Stellar Wave",
        "body": """## Description
Allow merchants to 'delete' their accounts while preserving their transaction history for audit purposes.

## Requirements and context
- Add `deleted_at` column to `merchants`.
- Filter out deleted merchants from standard queries.
- Block access for deleted merchant API keys.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/merchant-soft-delete`
- **Implement changes:**
  - Update schema and middlewares.
- **Test and commit:**
  - Verify the merchant is hidden and inaccessible after deletion.

## Example commit message
`feat: implement soft delete support for merchants`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] DX: Build Interactive CLI Tool for Testnet Simulation",
        "labels": "backend,dx,stellar,complexity:medium,Stellar Wave",
        "body": """## Description
Build a small internal CLI tool to help developers simulate payments on Testnet for local integration testing.

## Requirements and context
- Scripts to create keys, fund accounts via Friendbot, and send payments with specific memos.
- Use `commander.js`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b tool/testnet-simulator`
- **Implement changes:**
  - Add script to `backend/scripts/simulate.js`.
- **Test and commit:**
  - Use the tool to successfully confirm a local payment intent.

## Example commit message
`feat: add CLI tool for Stellar testnet payment simulation`

## Guidelines
- Complexity: Medium (150 points)"""
    },

    # --- FRONTEND (25) ---
    {
        "title": "[FE] Dashboard: Move Dashboard Home to dedicated /dashboard route",
        "labels": "frontend,refactor,ux,complexity:medium,Stellar Wave",
        "body": """## Description
Separate the public landing page from the authenticated dashboard management area.

## Requirements and context
- Move the current `/` logic to `/dashboard`.
- Build a new landing page (marketing focus) at `/`.
- Implement redirects for authenticated users.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b refactor/dashboard-routes`
- **Implement changes:**
  - Update Next.js page structure.
  - Implement middleware-based redirection.
- **Test and commit:**
  - Verify that `/dashboard` requires login and `/` is accessible to everyone.

## Example commit message
`refactor: separate marketing home from merchant dashboard`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Payment Logic: Implement Real-time Polking-based Feedback on Checkout",
        "labels": "frontend,ux,stellar,complexity:medium,Stellar Wave",
        "body": """## Description
Provide immediate feedback to the customer on the checkout page when their payment is detected and confirmed on-chain.

## Requirements and context
- Polling `GET /api/payments/:id` every 3 seconds while on checkout.
- Transition from 'Waiting for Payment' to 'Success' state automatically.
- Show transaction confetti on success.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/checkout-realtime-status`
- **Implement changes:**
  - Update `frontend/src/app/(public)/pay/[id]/page.tsx`.
- **Test and commit:**
  - Perform a payment and verify the UI updates without manual refresh.

## Example commit message
`feat: implement real-time payment status updates in checkout UI`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] UI Library: Build Skeleton Loading for Metrics Cards",
        "labels": "frontend,ux,design,complexity:trivial,Stellar Wave",
        "body": """## Description
Improve the perceived performance of the dashboard by showing skeleton loaders while metrics data is being fetched.

## Requirements and context
- Use `react-loading-skeleton`.
- Match the layout of `PaymentMetrics.tsx`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/metrics-skeletons`
- **Implement changes:**
  - Create `MetricsSkeleton.tsx`.
  - Update the metrics container to show skeletons during loading states.
- **Test and commit:**
  - Slow down the network and verify the skeletons render correctly.

## Example commit message
`ui: add skeleton loading states to dashboard metrics`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Settings: API Key Copy To Clipboard with UI Feedback",
        "labels": "frontend,ux,complexity:trivial,Stellar Wave",
        "body": """## Description
Make it easier for developers to manage their API keys by adding a reliable 'copy to clipboard' button with visual success feedback.

## Requirements and context
- Use `navigator.clipboard`.
- Show a success toast or icon change on copy.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/copy-api-key`
- **Implement changes:**
  - Update `ApiKeysPage.tsx`.
- **Test and commit:**
  - Verify the key is correctly copied to the clipboard.

## Example commit message
`ui: add copy-to-clipboard button with feedback for API keys`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Checkout: Localize Checkout Page to Spanish (ES) and Portuguese (PT)",
        "labels": "frontend,i18n,complexity:medium,Stellar Wave",
        "body": """## Description
Expand the reach of our payment links by localizing the checkout experience for the LATAM market.

## Requirements and context
- Use `next-intl` or similar.
- Translate: 'Total Amount', 'Asset', 'Waiting for Payment', 'Confirming', 'Payment Successful'.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b i18n/latam-checkout`
- **Implement changes:**
  - Add translation JSONs.
  - Wrap checkout components in i18n providers.
- **Test and commit:**
  - Verify translations load based on browser language or selector.

## Example commit message
`feat: localize checkout UI for Spanish and Portuguese`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Branding: Dynamic Checkout Colors based on Merchant Config",
        "labels": "frontend,design,ux,complexity:medium,Stellar Wave",
        "body": """## Description
Apply merchant-specific branding (primary colors and logos) to the public checkout page.

## Requirements and context
- Fetch branding config from the backend.
- Use CSS variables to inject custom colors into Tailwind theme.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/dynamic-checkout-branding`
- **Implement changes:**
  - Update `frontend/src/app/(public)/pay/[id]/page.tsx` to handle branding data.
- **Test and commit:**
  - Change branding in the database and verify the checkout page reflects changes.

## Example commit message
`feat: implement dynamic merchant branding for checkout pages`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Dashboard: Add Search and Pagination to Payment Table",
        "labels": "frontend,api,ux,complexity:high,Stellar Wave",
        "body": """## Description
Improve manageability of large datasets by adding server-side search and pagination to the payments list.

## Requirements and context
- Search by `recipient` or `amount`.
- Implement page buttons and 'items per page' selector.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/paginated-payment-table`
- **Implement changes:**
  - Update backend endpoints to support `?page=&limit=&q=`.
  - Refactor frontend table to use query parameters.
- **Test and commit:**
  - Verify search results and page transitions are smooth.

## Example commit message
`feat: add server-side search and pagination to payments dashboard`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] UI: Implement Animated Success State for Payment Creation",
        "labels": "frontend,design,ux,complexity:trivial,Stellar Wave",
        "body": """## Description
Make the payment link generation feel more premium with a smooth success transition and confetti effect.

## Requirements and context
- Use `framer-motion` for transitions.
- Integrate `canvas-confetti`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/payment-creation-feedback`
- **Implement changes:**
  - Update `CreatePaymentForm.tsx`.
- **Test and commit:**
  - Create an intent and verify the animation sequence.

## Example commit message
`ui: add animated success state for payment link generation`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Desktop: Global Dashboard Sidebar Component",
        "labels": "frontend,ux,design,complexity:medium,Stellar Wave",
        "body": """## Description
Establish a consistent navigation structure for authenticated users using a sidebar rather than only a top navigation bar.

## Requirements and context
- Icons for: Overview, Payments, Webhook Logs, Settings.
- Responsive behavior: Collapsible on desktop, drawer on mobile.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/dashboard-sidebar`
- **Implement changes:**
  - Create `src/components/Sidebar.tsx`.
- **Test and commit:**
  - Verify smooth navigation across all dashboard sub-pages.

## Example commit message
`ui: implement persistent dashboard navigation sidebar`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Checkout: Show Stellar.expert Link after Confirmation",
        "labels": "frontend,stellar,dx,complexity:trivial,Stellar Wave",
        "body": """## Description
Provide transparency to customers by linking to the transaction on the block explorer once confirmed.

## Requirements and context
- Use `stellar.expert` as the default explorer.
- Open link in a new tab.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/explorer-link`
- **Implement changes:**
  - Update the success view in the checkout page.
- **Test and commit:**
  - Click the link after a successful payment and verify it opens the correct transaction ID.

## Example commit message
`feat: add block explorer links to checkout success view`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Monitoring: Front-end Session Recording with Sentry Replay",
        "labels": "frontend,monitoring,ux,complexity:medium,Stellar Wave",
        "body": """## Description
Integrate Sentry Session Replay to debug user frustrations and UI crashes in real-time.

## Requirements and context
- Replay: Catch user clicks, scrolls, and errors.
- Mask PII automatically.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/sentry-replay`
- **Implement changes:**
  - Update Sentry configuration in `sentry.client.config.ts`.
- **Test and commit:**
  - Verify replays are being captured in the Sentry Dashboard.

## Example commit message
`feat: enable Sentry Session Replay for frontend monitoring`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Documentation: Migration to MDX for Static Docs",
        "labels": "frontend,dx,documentation,complexity:high,Stellar Wave",
        "body": """## Description
Transform the documentation area into a powerful developer portal using MDX to allow interactive code examples.

## Requirements and context
- Use `next-mdx-remote` or similar.
- Implement a documentation layout with a nested sidebar.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b docs/mdx-migration`
- **Implement changes:**
  - Convert markdown files to `.mdx`.
  - Add syntax highlighting support (`rehype-prism-plus`).
- **Test and commit:**
  - Verify docs render correctly and code blocks are highlighted.

## Example commit message
`docs: migrate documentation to MDX with syntax highlighting`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Performance: Multi-Region Edge Caching for Asset Metadata",
        "labels": "frontend,performance,complexity:high,Stellar Wave",
        "body": """## Description
Optimize the loading of common asset metadata (XLM/USDC logos and names) using Next.js Incremental Static Regeneration (ISR).

## Requirements and context
- Cache asset data at the edge for 1 hour.
- Reduce re-validation calls to Horizon.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b perf/asset-metadata-cache`
- **Implement changes:**
  - Implement ISR in dashboard components fetching asset info.
- **Test and commit:**
  - Measure first-page load speed with and without caching.

## Example commit message
`perf: implement ISR for asset metadata edge caching`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Mobile: Responsive Bottom Navigation for PWA support",
        "labels": "frontend,mobile,ux,complexity:medium,Stellar Wave",
        "body": """## Description
Enhance the mobile experience by adding a standard bottom navigation bar when viewed on small screens.

## Requirements and context
- Hide sidebar on mobile.
- Bottom bar icons: Home, Payments, Create, Settings.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/mobile-bottom-nav`
- **Implement changes:**
  - Create `src/components/MobileNav.tsx`.
- **Test and commit:**
  - Use Chrome DevTools mobile view and verify accessibility and touch target size.

## Example commit message
`ui: add responsive bottom navigation for mobile users`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Testing: Build Comprehensive E2E Test Suite for Checkout",
        "labels": "frontend,testing,qa,complexity:high,Stellar Wave",
        "body": """## Description
Implement a Playwright test suite to ensure the critical checkout path never breaks.

## Requirements and context
- Tests: Rendering, QR code visibility, Wallet select modal, Error handling.
- Run on multiple browsers (Chromium, Firefox, Webkit).

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b test/playback-checkout-e2e`
- **Implement changes:**
  - Create `tests/checkout.spec.ts`.
- **Test and commit:**
  - Run the tests locally and in CI to verify stability.

## Example commit message
`test: implement E2E checkouts suite with Playwright`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Add 'Pay with QR code' Modal with Download button",
        "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave",
        "body": """## Description
Allow users to easily download the payment QR code to scan it on another device or share it via chat.

## Requirements and context
- Add a download icon to the QR component.
- Support PNG export.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/qr-download`
- **Implement changes:**
  - Add download logic using a canvas referer.
- **Test and commit:**
  - Verify the downloaded image is clear and can be scanned.

## Example commit message
`feat: add QR code download functionality to checkout`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Dashboard: Charting - Add Weekly Average Volume",
        "labels": "frontend,analytics,ux,complexity:medium,Stellar Wave",
        "body": """## Description
Help merchants identify trends by showing a weekly rolling average on their volume charts.

## Requirements and context
- Use `recharts` to add a secondary trend line.
- Calculate moving average in the dashboard hooks.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b analytics/weekly-average`
- **Implement changes:**
  - Update `PaymentMetrics.tsx`.
- **Test and commit:**
  - Verify the trend line calculation matches the raw data points.

## Example commit message
`feat: add weekly average trend line to metrics chart`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Accessability: Pass WCAG 2.1 Contrast Guidelines for Dashboard",
        "labels": "frontend,accessibility,bug,complexity:medium,Stellar Wave",
        "body": """## Description
Audit and fix accessibility issues across the dashboard to ensure compliance with WCAG 2.1 standards.

## Requirements and context
- Fix contrast ratios for muted text.
- Ensure all interactive elements have correct `aria-label` attributes.
- Keyboard navigation check.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b accessibility/dashboard-audit`
- **Implement changes:**
  - Audit using Lighthouse or axe-core.
  - Apply color and ARIA fixes.
- **Test and commit:**
  - Verify Lighthouse accessibility score is 100.

## Example commit message
`fix: improve dashboard accessibility to meet WCAG 2.1 compliance`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Settings: Merchant Domain Verification for Webhooks",
        "labels": "frontend,security,feature,complexity:high,Stellar Wave",
        "body": """## Description
Implement a domain verification flow for webhooks to ensure that merchants actually control the endpoints they are configuring.

## Requirements and context
- File-based verification (`/.well-known/stellar-pay-verification.txt`).
- Dashboard UI showing 'Verified' or 'Unverified' status.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/domain-verification`
- **Implement changes:**
  - Add verification logic to backend and frontend settings UI.
- **Test and commit:**
  - Verify that a domain is only marked as verified if the token matches.

## Example commit message
`feat: implement domain verification for merchant webhooks`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Show Stellar Fee Breakdown in Modal",
        "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave",
        "body": """## Description
Provide transparency to the user by showing the estimated network fees (stroops) for their transaction before they pay.

## Requirements and context
- Fetch current Testnet/Mainnet fee stats.
- Show 'Network Fee: ~0.00001 XLM' in the checkout modal.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/fee-transparency`
- **Implement changes:**
  - Use `server.feeStats()` from StellarSDK.
- **Test and commit:**
  - Verify the fee updates in response to network demand.

## Example commit message
`ui: show transparent Stellar network fee estimate on checkout`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Dashboard: Add Multi-Select for Bulk Webhook Retries",
        "labels": "frontend,ux,api,complexity:medium,Stellar Wave",
        "body": """## Description
Save merchant time by allowing them to select multiple failed webhooks from the logs and retry them all in one click.

## Requirements and context
- Add checkboxes to the Webhook Logs table.
- Implement `POST /api/webhooks/retry-bulk`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/bulk-webhook-retry`
- **Implement changes:**
  - Update table UI and add bulk retry action.
- **Test and commit:**
  - Verify that all selected logs are correctly queued for retry.

## Example commit message
`feat: add bulk retry functionality to webhook logs`

## Guidelines
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] UI: Implement Copy-Button with 'Glitch' Animation on Success",
        "labels": "frontend,design,ux,complexity:trivial,Stellar Wave",
        "body": """## Description
Add a unique, on-brand 'glitch' animation to the copy button when a copy is successful, matching our premium dark/hacker aesthetic.

## Requirements and context
- Use `framer-motion` keyframes.
- Apply to `CopyButton` component.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/glitch-copy-feedback`
- **Implement changes:**
  - Add animation variants to the button.
- **Test and commit:**
  - Copy an item and verify the visual effect.

## Example commit message
`ui: add premium glitch animation to copy button feedback`

## Guidelines
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[FE] Branding: Support for Light Theme (Experimental Toggle)",
        "labels": "frontend,design,feature,complexity:high,Stellar Wave",
        "body": """## Description
Implement an experimental light theme toggle for merchants who prefer light mode, ensuring accessibility and flexibility.

## Requirements and context
- Use CSS Variables or Tailwind dark: prefix.
- Store preference in localStorage.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b ui/light-mode-support`
- **Implement changes:**
  - Add theme toggle to header.
  - Define light-mode color palette.
- **Test and commit:**
  - Toggle themes and verify no unreadable text exists in either mode.

## Example commit message
`feat: implement experimental light theme support`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Checkout: Show 'Pay in XLM' even if Invoice is USDC (using path payments)",
        "labels": "frontend,stellar,ux,complexity:high,Stellar Wave",
        "body": """## Description
Increase conversion by allowing users to pay with their native XLM even if the merchant expects USDC, leveraging Stellar Path Payments under the hood.

## Requirements and context
- Detect optimal paths for conversion.
- Show 'Approximate cost in XLM' at checkout.
- Execute path payment via Freighter/WalletConnect.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b feature/checkout-path-payment`
- **Implement changes:**
  - Integrate path discovery in the checkout page.
- **Test and commit:**
  - Complete an XLM->USDC payment flow successfully.

## Example commit message
`feat: support paying in XLM for USDC invoices via path payments`

## Guidelines
- Complexity: High (200 points)"""
    },
    {
        "title": "[FE] Testing: Add Visual Regression Tests with Playwright",
        "labels": "frontend,testing,qa,complexity:medium,Stellar Wave",
        "body": """## Description
Set up basic visual regression testing for critical components to ensure that UI changes don't cause unexpected regressions.

## Requirements and context
- Use `playwright` visual comparison.
- Capture: Dashboard Home, Checkout, Settings.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b test/visual-regression`
- **Implement changes:**
  - Add visual test scripts.
- **Test and commit:**
  - Verify a deliberate change triggers a test failure.

## Example commit message
`test: add visual regression testing for critical dashboard paths`

## Guidelines
- Complexity: Medium (150 points)"""
    }
]

print(f"Creating 50 NEW batch issues (Numbers 273-322)...")
for i, issue in enumerate(issues, start=273):
    cmd = [
        gh_path, "issue", "create", 
        "--repo", repo, 
        "--title", f"{issue['title']}", 
        "--body", f"{issue['body']}", 
        "--label", f"{issue['labels']}"
    ]
    print(f"[{i}] Creating: {issue['title']}")
    subprocess.Popen(cmd).wait()
    time.sleep(1.2)

print("\nAll 50 issues have been successfully pushed to the repository!")
