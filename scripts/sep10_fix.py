import subprocess
import time
import os

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

failures_issues = [
    {
        "title": "[BE] Critical: Fix ES Module Caching Bug in SEP-0010 Tests",
        "labels": "backend,bug,stellar,testing,critical,complexity:medium",
        "body": """## Description
The backend test suite is currently failing with 5 errors in `src/lib/sep10-auth.test.js` indicating: `Error: SEP-0010 server signing key not configured`. This is a module evaluation bug caused by `import` statements loading and caching environment variables before Vitest's `beforeAll` can mutate them.

## Requirements and context
- **Failed Tests:** All 5 tests inside `backend/src/lib/sep10-auth.test.js`.
- **Problem Area:** In `sep10-auth.js`, the `SERVER_SIGNING_KEY` is captured directly at the module-level from `process.env`. In the test file, `process.env.SEP10_SERVER_SIGNING_KEY` is being set *after* the import completes, causing the test environment to crash.
- **Solution:** You need to refactor the authentication module to dynamically resolve the environment variable during function execution, or use `vi.stubEnv` combined with dynamic imports to properly mock module-level secrets.

## Suggested execution
- **Fork the repo and create a branch:** git checkout -b fix/sep10-test-caching
- **Implement changes:**
  - Update `backend/src/lib/sep10-auth.js` to read `process.env.SEP10_SERVER_SIGNING_KEY` dynamically inside `generateChallenge` and `verifyChallenge`, OR refactor how the environment is managed during tests.
  - Remove module-level capturing of dynamic secrets.
- **Test and commit:**
  - Run `npm run test` inside the `backend` directory.
  - Verify that `Tests 72 passed` (0 failures).

## Example commit message
fix: resolved module caching bug in SEP-0010 authentication tests

## Guidelines
- This is a deployment blocker, High Priority.
- Focus Area: `backend/src/lib/sep10-auth.js` and `backend/src/lib/sep10-auth.test.js`.
- Complexity: Medium (150 points)"""
    }
]

print(f"Creating {len(failures_issues)} CRITICAL test-focused issues...")
for issue in failures_issues:
    cmd = [
        gh_path, "issue", "create", 
        "--repo", repo, 
        "--title", issue["title"], 
        "--body", issue["body"]
    ]
    # Handle labels manually to avoid missing label errors by recreating them if needed
    labels = issue["labels"].split(",")
    for label in labels:
        cmd.extend(["--label", label.strip()])
        
    print(f"Creating: {issue['title']}")
    subprocess.Popen(cmd).wait()
    time.sleep(1.5)

print("Done!")
