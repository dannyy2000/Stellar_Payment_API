import subprocess
import time
import os

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

critical_failures = [
    {
        "title": "[FE] Critical: Fix Application Startup Crash (Runtime Error 500)",
        "labels": "frontend,bug,critical,complexity:medium",
        "body": """## Description
The React application fails to render any page (`GET / 500`) due to a missing environmental configuration file and a runtime crash in the dynamic `@walletconnect/sign-client` loader. This is a deployment blocker.

## Requirements and context
- **Missing Env:** No `.env` file exists in the `frontend` root. The application depends on `NEXT_PUBLIC_API_URL` to fetch merchant data.
- **Runtime Crash:** The file `src/lib/wallet-walletconnect.ts` tries to dynamic-import `@walletconnect/sign-client` which is not installed in `node_modules` or listed in `package.json`.
- **Validation:** The startup check should fail gracefully instead of crashing the process if the WalletConnect project ID is missing.

## Suggested execution
- **Fork the repo and create a branch:** git checkout -b fix/startup-crash
- **Implement changes:**
  - Create a default `.env` based on `.env.example`.
  - Install both `@walletconnect/sign-client` and `@walletconnect/types`.
  - Add a guard in `wallet-walletconnect.ts` to skip loading if `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` is not set.
- **Test and commit:**
  - Run `npm run dev` and visit `http://localhost:3000`.
  - Verify the page loads successfully without a 500 error.

## Example commit message
fix: resolved 500 startup crash and missing ENV vars

## Guidelines
- Focus Area: `frontend/.env`, `frontend/package.json`, `frontend/src/lib/wallet-walletconnect.ts`.
- Assignment required before starting.
- Complexity: Medium (150 points)"""
    }
]

print(f"Creating 1 CRITICAL failure issue...")
for issue in critical_failures:
    cmd = [
        gh_path, "issue", "create", 
        "--repo", repo, 
        "--title", issue["title"], 
        "--body", issue["body"], 
        "--label", issue["labels"]
    ]
    print(f"Creating: {issue['title']}")
    subprocess.Popen(cmd).wait()
    time.sleep(1.5)

print("Done!")
