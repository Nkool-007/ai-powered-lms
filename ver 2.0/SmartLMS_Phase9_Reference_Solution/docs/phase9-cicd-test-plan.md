# SmartLMS — Phase 9 CI/CD Test Plan

> Important: the expected reference outcome is PASS. Students must record the result actually observed in their repository. Do not write PASS without executing the test.

## Test 1 — Workflow Runs on Push

**Procedure**

1. Push a harmless commit to an approved branch.
2. Open GitHub Actions.

**Expected**

SmartLMS CI starts automatically.

**Actual Result**

TO BE EXECUTED

---

## Test 2 — Workflow Runs on Pull Request

**Procedure**

1. Create a feature branch.
2. Open a PR to `develop`.
3. Check PR status.

**Expected**

Backend CI and Frontend CI appear.

**Actual Result**

TO BE EXECUTED

---

## Test 3 — Backend Dependencies Install

**Expected**

`pip install -r backend/requirements-ci.txt` succeeds.

**Actual Result**

TO BE EXECUTED

---

## Test 4 — Backend Lint Runs

**Expected**

`ruff check` executes and returns success for valid code.

**Actual Result**

TO BE EXECUTED

---

## Test 5 — Backend Tests Run

**Expected**

pytest executes the backend test suite.

**Actual Result**

TO BE EXECUTED

---

## Test 6 — Failed Backend Test Fails CI

**Procedure**

Temporarily introduce one controlled failing test.

**Expected**

Backend CI becomes FAILED.

**Actual Result**

TO BE EXECUTED

---

## Test 7 — Frontend Dependencies Install

**Expected**

`npm ci` succeeds from the committed package-lock.

**Actual Result**

TO BE EXECUTED

---

## Test 8 — Frontend Lint Runs

**Expected**

`npm run lint` executes.

**Actual Result**

TO BE EXECUTED

---

## Test 9 — Frontend Tests Run

**Expected**

`npm run test` executes Vitest.

**Actual Result**

TO BE EXECUTED

---

## Test 10 — React Production Build Succeeds

**Expected**

`npm run build` creates `dist/`.

**Actual Result**

TO BE EXECUTED

---

## Test 11 — Failed Frontend Check Fails CI

**Procedure**

Temporarily create a frontend lint/test failure.

**Expected**

Frontend CI becomes FAILED.

**Actual Result**

TO BE EXECUTED

---

## Test 12 — AI Tests Do Not Require Real Paid Provider

**Procedure**

Inspect AI tests and CI provider configuration.

**Expected**

Mocked provider responses are used.

**Actual Result**

TO BE EXECUTED

---

## Test 13 — Production Secrets Are Not Present in Workflow YAML

Inspect `.github/workflows/`.

**Expected**

No production credential values exist.

**Actual Result**

TO BE EXECUTED

---

## Test 14 — Pull Request Displays CI Status

**Expected**

PR shows GitHub Actions checks.

**Actual Result**

TO BE EXECUTED

---

## Test 15 — Valid Commit Passes All Mandatory Checks

**Expected**

- Backend CI = PASS
- Frontend CI = PASS

**Actual Result**

TO BE EXECUTED

---

# Advanced Tests

## Test 16 — Docker Image Builds Automatically

**Expected**

Backend image is built only after successful CI.

**Actual Result**

NOT APPLICABLE unless advanced CD is implemented.

---

## Test 17 — Docker Image Pushes to Registry

**Expected**

Commit-tagged image appears in ECR.

**Actual Result**

NOT APPLICABLE unless advanced CD is implemented.

---

## Test 18 — Deployment Runs Only After Successful CI

**Expected**

Failed CI does not trigger production deployment.

**Actual Result**

NOT APPLICABLE unless advanced CD is implemented.

---

## Test 19 — Frontend Deployment Updates S3/CloudFront

**Expected**

Approved frontend build is uploaded and cache invalidated.

**Actual Result**

NOT APPLICABLE unless advanced CD is implemented.

---

## Test 20 — Deployment Health Check Succeeds

**Expected**

Production health endpoint returns success after deployment.

**Actual Result**

NOT APPLICABLE unless advanced CD is implemented.
