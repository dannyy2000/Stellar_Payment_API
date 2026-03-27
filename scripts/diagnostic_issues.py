import subprocess
import time
import os

repo = "emdevelopa/Stellar_Payment_API"
gh_path = os.path.expanduser("~/.local/bin/gh")
if not os.path.exists(gh_path):
    gh_path = "gh"

# First create any missing labels
labels_to_create = [
    ("critical", "d93f0b", "Critical blocker issues"),
    ("robustness", "0052cc", "Reliability improvements"),
    ("infra", "c5def5", "Infrastructure setup"),
    ("config", "e4e669", "Configuration issues"),
]

for name, color, desc in labels_to_create:
    subprocess.run([
        gh_path, "label", "create", name,
        "--repo", repo, "-c", color, "-d", desc, "--force"
    ], capture_output=True)

issues = [
    {
        "title": "[BE] Critical: Backend Cannot Start — Missing socket.io Dependency",
        "labels": ["backend", "bug", "critical", "complexity:trivial"],
        "body": """## Description
The backend server crashes immediately on startup with:
```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'socket.io'
```
`socket.io` is listed in `package.json` but is not installed in `node_modules` after a fresh `npm install`. This crashes the entire API before it can handle any requests.

## Requirements and context
- `socket.io` must be declared in `backend/package.json` under `dependencies` and be resolved on a fresh `npm install`.
- The package-lock.json must be committed so downstream contributors don't hit this.
- Verify the server starts cleanly after the fix: `npm run dev` should print `API listening on http://localhost:4000`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/missing-socket-io`
- **Implement changes:**
  - Run `npm install socket.io` inside the `backend/` directory.
  - Commit the updated `package.json` and `package-lock.json`.
- **Test and commit:**
  - Run `npm run dev` and confirm no crash.
  - Run `npm run test` to make sure nothing else breaks.

## Example commit message
```
fix: add socket.io to backend dependencies
```

## Guidelines
- Focus Area: `backend/package.json` and `backend/package-lock.json`.
- This is a **launch blocker** — contributors cannot run the API without this fix.
- Assignment required before starting.
- PR description must include: `Closes #[issue_id]`
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Critical: Backend Crashes on Startup Without .env File",
        "labels": ["backend", "bug", "critical", "config", "complexity:trivial"],
        "body": """## Description
Running `npm run dev` in the backend directory immediately crashes with:
```
Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY
```
The codebase validates environment variables at module-load time. New contributors who clone the repo and run the server have no `.env` file, causing an instant, unhelpful crash.

## Requirements and context
- The `.env.example` file exists at `backend/.env.example` but is not copied or documented clearly in the README.
- `backend/src/lib/env-validation.js` throws at startup if keys are missing, blocking first-time setup.
- A graceful startup mode with clear messaging is needed for local development.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/env-startup-ux`
- **Implement changes:**
  - Update the README's "Getting Started" section with a clear `cp .env.example .env` step.
  - Improve the error message in `backend/src/lib/env-validation.js` to print a link to the docs/`.env.example` rather than a bare throw.
  - Consider adding a `--dry-run` or graceful degradation mode for when Supabase keys are absent (e.g. skip DB routes, still serve `/health`).
- **Test and commit:**
  - Verify `npm run dev` gives a helpful human-readable message when `.env` is missing.

## Example commit message
```
fix: improve startup error UX when .env is missing
```

## Guidelines
- Focus Area: `backend/src/lib/env-validation.js` and `backend/README.md`.
- This affects every new contributor's first experience.
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Fix: SEP-0010 Tests Fail Due to ES Module Signing Key Caching",
        "labels": ["backend", "bug", "stellar", "testing", "complexity:medium"],
        "body": """## Description
All 5 tests in `backend/src/lib/sep10-auth.test.js` fail with:
```
Error: SEP-0010 server signing key not configured
```
The test file sets `process.env.SEP10_SERVER_SIGNING_KEY` inside `beforeAll()`, but `sep10-auth.js` reads the key **at module evaluation time** (top-level const). Because ES Modules are evaluated once and cached, the env var is always `undefined` when the module loads, even though `beforeAll` correctly sets it later.

## Requirements and context
- `backend/src/lib/sep10-auth.js` captures `SERVER_SIGNING_KEY` at the top level before any test lifecycle hook can set it.
- The fix requires making the key lookup **lazy** (read inside each function call) so Vitest's `beforeAll` patches land in time.
- All 5 tests must pass after the fix with `npm run test`.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/sep10-lazy-env`
- **Implement changes:**
  - Remove the top-level `const SERVER_SIGNING_KEY = process.env.SEP10_SERVER_SIGNING_KEY`.
  - Inside `generateChallenge()` and `verifyChallenge()`, read `process.env.SEP10_SERVER_SIGNING_KEY` directly at call time.
  - Alternatively use `vi.stubEnv` in the test file for a test-only approach.
- **Test and commit:**
  - Run `npm run test` — confirm `Tests 72 passed` with 0 failures from `sep10-auth.test.js`.

## Example commit message
```
fix: lazy-load SEP10_SERVER_SIGNING_KEY to fix env caching in tests
```

## Guidelines
- Focus Area: `backend/src/lib/sep10-auth.js` (lines 15-18).
- Do NOT change the test file structure unless the test approach itself is wrong.
- Complexity: Medium (150 points)"""
    },
    {
        "title": "[FE] Performance: Replace <img> Tags with next/image in HeroSection",
        "labels": ["frontend", "bug", "ux", "complexity:trivial"],
        "body": """## Description
The linter (`npm run lint`) currently reports 3 warnings in `HeroSection.tsx`:
```
Using <img> could result in slower LCP and higher bandwidth. Consider using <Image /> from next/image
```
While these are warnings (not errors), they indicate suboptimal images that will hurt Core Web Vitals scores (LCP) and bandwidth costs in production. This is a quick but impactful performance win.

## Requirements and context
- Replace every `<img>` tag at lines 44, 45, 46 of `src/components/login/HeroSection.tsx` with the Next.js `<Image />` component.
- Provide appropriate `width`, `height`, and `alt` props for accessibility.
- Ensure layout is not broken after the change (visual regression check).

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/hero-next-image`
- **Implement changes:**
  - Import `Image` from `next/image` at the top of `HeroSection.tsx`.
  - Replace the 3 `<img>` tags with `<Image>` components.
  - Add `width`, `height`, and `alt` attributes.
- **Test and commit:**
  - Run `npm run lint` — confirm 0 warnings from `HeroSection.tsx`.
  - Check the login page at `localhost:3000/login` and verify layout is intact.

## Example commit message
```
perf: replace <img> with next/image in HeroSection for better LCP
```

## Guidelines
- Focus Area: `frontend/src/components/login/HeroSection.tsx` (lines 44–46).
- Include before/after screenshot in the PR.
- PR description must include: `Closes #[issue_id]`
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Infrastructure: Document Redis Setup Requirement for Local Development",
        "labels": ["backend", "infra", "dx", "complexity:trivial"],
        "body": """## Description
The backend requires a running Redis instance for distributed rate-limiting (`REDIS_URL=redis://localhost:6379`). There is no mention of this prerequisite in the README or developer setup guide. Contributors who attempt to run the backend without Redis will see connection errors silently degrading the rate-limiter, or worse, crashing requests.

## Requirements and context
- Redis is required by `backend/src/lib/redis.js` and `backend/src/lib/rate-limit.js`.
- The `.env.example` lists `REDIS_URL` but doesn't explain how to run Redis locally.
- New contributors need a simple `docker run` or `brew install redis` step to get unblocked.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b docs/redis-setup`
- **Implement changes:**
  - Update `backend/README.md` with a "Prerequisites" section listing Node.js, Redis, and a Supabase account.
  - Add a quick `docker-compose.yml` to the `backend/` directory for one-command Redis + API startup.
  - Optionally add a `redis.check.js` helper that prints a human-readable message if Redis is unavailable.
- **Test and commit:**
  - Verify a contributor can start both Redis and the API by following the README steps alone.

## Example commit message
```
docs: add Redis setup instructions and docker-compose for local dev
```

## Guidelines
- Focus Area: `backend/README.md` and optionally `backend/docker-compose.yml`.
- Complexity: Trivial (100 points)"""
    },
    {
        "title": "[BE] Fix: RLS Integration Tests Require Active Database Connection",
        "labels": ["backend", "testing", "infra", "complexity:medium"],
        "body": """## Description
`backend/src/lib/rls.test.js` contains critical Row Level Security integration tests that are always **skipped** in CI because `DATABASE_URL` is not set. While the `skipIf` guard is correct (prevents crashes), the tests never actually run to validate the security policies.

## Requirements and context
- The tests in `rls.test.js` create real DB rows and verify cross-merchant data isolation.
- They are skipped with `describe.skipIf(!DB_URL)` when `DATABASE_URL` env var is absent.
- We need a CI-safe way to run these tests, such as using a test Supabase project or a local Postgres container.

## Suggested execution
- **Fork the repo and create a branch:** `git checkout -b fix/rls-ci-tests`
- **Implement changes:**
  - Add a GitHub Actions workflow step that spins up a local Postgres container and applies the SQL schema.
  - Or document in the README how to run the RLS tests locally with a real DB connection.
  - Ensure `rls.test.js` is listed in the test run summary as passing (not skipped).
- **Test and commit:**
  - Run `DATABASE_URL=<your-local-db> npm run test` and confirm RLS tests pass.

## Example commit message
```
test: enable RLS integration tests with a ephemeral postgres container
```

## Guidelines
- Focus Area: `backend/src/lib/rls.test.js` and `.github/workflows/`.
- The RLS security guarantees are mission-critical — these tests must run somewhere.
- Complexity: Medium (150 points)"""
    },
]

print(f"Creating {len(issues)} diagnostic issues based on live test run...")
for issue in issues:
    cmd = [gh_path, "issue", "create", "--repo", repo,
           "--title", issue["title"], "--body", issue["body"]]
    for label in issue["labels"]:
        cmd += ["--label", label]
    print(f"  → {issue['title'][:70]}...")
    subprocess.Popen(cmd).wait()
    time.sleep(1.2)

print("\nAll issues pushed!")
