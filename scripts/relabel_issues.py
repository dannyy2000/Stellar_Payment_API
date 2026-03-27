import subprocess
import json
import os

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

# ────────────── ORIGINAL 50 TITLES AND LABELS ──────────────
issues_metadata = [
    {"title": "[BE] Implement SEP-0001 (stellar.toml) Generator", "labels": "backend,stellar,enhancement,complexity:medium,Stellar Wave"},
    {"title": "[BE] Asset Conversion: Implement Path Payments in Verification", "labels": "backend,stellar,enhancement,complexity:high,Stellar Wave"},
    {"title": "[BE] Data Retention: Automated DB Archival for Old Payment Intents", "labels": "backend,database,maintenance,complexity:medium,Stellar Wave"},
    {"title": "[BE] Security: Rate Limit Endpoint for Merchant Registration", "labels": "backend,security,bug,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Monitoring: Integration with Sentry for Backend Error Tracking", "labels": "backend,monitoring,dx,complexity:medium,Stellar Wave"},
    {"title": "[BE] API: Build Endpoint for Merchant Branding Customization", "labels": "backend,api,enhancement,complexity:medium,Stellar Wave"},
    {"title": "[BE] Validation: Strict Type Check for Stellar Memos", "labels": "backend,bug,stellar,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Scalability: Connection Pooling Optimization for PG", "labels": "backend,performance,database,complexity:medium,Stellar Wave"},
    {"title": "[BE] Audit: Log Merchant Login Attempts", "labels": "backend,security,audit,complexity:medium,Stellar Wave"},
    {"title": "[BE] Integration: Implement Webhook Signature Header (HMAC-SHA256)", "labels": "backend,security,robustness,complexity:high,Stellar Wave"},
    {"title": "[BE] Testing: Build Integration Test Suite for Payment Lifecycle", "labels": "backend,testing,qa,complexity:high,Stellar Wave"},
    {"title": "[BE] Refactor: Extract Business Logic from Routes to Services", "labels": "backend,refactor,dx,complexity:medium,Stellar Wave"},
    {"title": "[BE] Documentation: Implement Automated API Docs with Swagger", "labels": "backend,dx,documentation,complexity:medium,Stellar Wave"},
    {"title": "[BE] Robustness: Implement Request Validation Middleware", "labels": "backend,robustness,security,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Monitoring: Custom Prometheus Metrics for Payment Volume", "labels": "backend,monitoring,metrics,complexity:medium,Stellar Wave"},
    {"title": "[BE] Database: Multi-Index Optimization for Payments Table", "labels": "backend,database,performance,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Security: Implement API Key Expiry and Rotation", "labels": "backend,security,api,complexity:high,Stellar Wave"},
    {"title": "[BE] Asset Support: Add USDC (Ethereum/AssetHub) Issuers to Default List", "labels": "backend,stellar,config,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Robustness: Implement Global Error Handling Middleware", "labels": "backend,robustness,dx,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Scaling: Implement Redis-based Idempotency Key Storage", "labels": "backend,scalability,robustness,complexity:high,Stellar Wave"},
    {"title": "[BE] Integration: Add Support for Webhook Retries with Exponential Backoff", "labels": "backend,robustness,complexity:high,Stellar Wave"},
    {"title": "[BE] API: Endpoint to Fetch Individual Payment Details (Extended)", "labels": "backend,api,enhancement,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Security: Sanitize Metadata Payloads to Prevent XSS", "labels": "backend,security,bug,complexity:trivial,Stellar Wave"},
    {"title": "[BE] Database: Implement Soft Deletes for Merchants", "labels": "backend,database,feature,complexity:trivial,Stellar Wave"},
    {"title": "[BE] DX: Build Interactive CLI Tool for Testnet Simulation", "labels": "backend,dx,stellar,complexity:medium,Stellar Wave"},
    {"title": "[FE] Dashboard: Move Dashboard Home to dedicated /dashboard route", "labels": "frontend,refactor,ux,complexity:medium,Stellar Wave"},
    {"title": "[FE] Payment Logic: Implement Real-time Polking-based Feedback on Checkout", "labels": "frontend,ux,stellar,complexity:medium,Stellar Wave"},
    {"title": "[FE] UI Library: Build Skeleton Loading for Metrics Cards", "labels": "frontend,ux,design,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Settings: API Key Copy To Clipboard with UI Feedback", "labels": "frontend,ux,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Checkout: Localize Checkout Page to Spanish (ES) and Portuguese (PT)", "labels": "frontend,i18n,complexity:medium,Stellar Wave"},
    {"title": "[FE] Branding: Dynamic Checkout Colors based on Merchant Config", "labels": "frontend,design,ux,complexity:medium,Stellar Wave"},
    {"title": "[FE] Dashboard: Add Search and Pagination to Payment Table", "labels": "frontend,api,ux,complexity:high,Stellar Wave"},
    {"title": "[FE] UI: Implement Animated Success State for Payment Creation", "labels": "frontend,design,ux,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Desktop: Global Dashboard Sidebar Component", "labels": "frontend,ux,design,complexity:medium,Stellar Wave"},
    {"title": "[FE] Checkout: Show Stellar.expert Link after Confirmation", "labels": "frontend,stellar,dx,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Monitoring: Front-end Session Recording with Sentry Replay", "labels": "frontend,monitoring,ux,complexity:medium,Stellar Wave"},
    {"title": "[FE] Documentation: Migration to MDX for Static Docs", "labels": "frontend,dx,documentation,complexity:high,Stellar Wave"},
    {"title": "[FE] Performance: Multi-Region Edge Caching for Asset Metadata", "labels": "frontend,performance,complexity:high,Stellar Wave"},
    {"title": "[FE] Mobile: Responsive Bottom Navigation for PWA support", "labels": "frontend,mobile,ux,complexity:medium,Stellar Wave"},
    {"title": "[FE] Testing: Build Comprehensive E2E Test Suite for Checkout", "labels": "frontend,testing,qa,complexity:high,Stellar Wave"},
    {"title": "[FE] Checkout: Add 'Pay with QR code' Modal with Download button", "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Dashboard: Charting - Add Weekly Average Volume", "labels": "frontend,analytics,ux,complexity:medium,Stellar Wave"},
    {"title": "[FE] Accessability: Pass WCAG 2.1 Contrast Guidelines for Dashboard", "labels": "frontend,accessibility,bug,complexity:medium,Stellar Wave"},
    {"title": "[FE] Settings: Merchant Domain Verification for Webhooks", "labels": "frontend,security,feature,complexity:high,Stellar Wave"},
    {"title": "[FE] Checkout: Show Stellar Fee Breakdown in Modal", "labels": "frontend,stellar,ux,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Dashboard: Add Multi-Select for Bulk Webhook Retries", "labels": "frontend,ux,api,complexity:medium,Stellar Wave"},
    {"title": "[FE] UI: Implement Copy-Button with 'Glitch' Animation on Success", "labels": "frontend,design,ux,complexity:trivial,Stellar Wave"},
    {"title": "[FE] Branding: Support for Light Theme (Experimental Toggle)", "labels": "frontend,design,feature,complexity:high,Stellar Wave"},
    {"title": "[FE] Checkout: Show 'Pay in XLM' even if Invoice is USDC (using path payments)", "labels": "frontend,stellar,ux,complexity:high,Stellar Wave"},
    {"title": "[FE] Testing: Add Visual Regression Tests with Playwright", "labels": "frontend,testing,qa,complexity:medium,Stellar Wave"}
]

print("Fetching latest issues...")
cmd_list = [gh_path, "issue", "list", "--repo", repo, "--limit", "100", "--state", "open", "--json", "number,title"]
result = subprocess.run(cmd_list, capture_output=True, text=True)
issues_on_gh = json.loads(result.stdout)

print(f"Applying labels to {len(issues_metadata)} issues...")
for issue_data in issues_metadata:
    # Find the issue number by title
    match = next((i for i in issues_on_gh if i["title"] == issue_data["title"]), None)
    if match:
        number = match["number"]
        labels = [l.strip() for l in issue_data["labels"].split(",")]
        
        print(f"Updating Issue #{number}: {issue_data['title']}")
        cmd_edit = [gh_path, "issue", "edit", str(number), "--repo", repo]
        for label in labels:
            cmd_edit.extend(["--add-label", label])
        
        subprocess.run(cmd_edit, capture_output=True)
    else:
        print(f"Could not find issue with title: {issue_data['title']}")

print("All issues relabeled successfully!")
