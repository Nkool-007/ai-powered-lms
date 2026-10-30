# SmartLMS — Phase 9 CI/CD Integration Notes

Students must keep only issues actually encountered in their own implementation.

The entries below are reference examples and must not be presented as real incidents unless they actually occurred.

## Issue Template

### Issue

Describe the issue.

### Observed Behaviour

What happened?

### Root Cause

Why did it happen?

### Affected Job

Backend CI / Frontend CI / Deployment.

### Solution

What was changed?

### Final Behaviour

What happened after the fix?

---

## Example Issue — Ruff Was Missing

### Observed Behaviour

Backend lint step failed with:

```text
ruff: command not found
```

### Root Cause

Ruff was not included in CI dependencies.

### Affected Job

Backend CI

### Solution

Created `backend/requirements-ci.txt` containing the application requirements plus Ruff.

### Final Behaviour

The backend lint step executes correctly.

---

## Example Issue — PostgreSQL Was Not Ready

### Observed Behaviour

pytest failed while creating the test schema.

### Root Cause

The database service had not become healthy.

### Affected Job

Backend CI

### Solution

Configured a PostgreSQL service health check with `pg_isready`.

### Final Behaviour

GitHub waits for the database service before backend checks proceed.

---

## Example Issue — pgvector Type Failed During Tests

### Observed Behaviour

AI database model initialization failed.

### Root Cause

The test PostgreSQL instance contained pgvector binaries but the `vector` extension had not been enabled.

### Affected Job

Backend CI

### Solution

Added:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

before pytest.

### Final Behaviour

CourseChunk vector columns can be created during CI.

---

## Example Issue — `npm ci` Failed

### Observed Behaviour

GitHub Actions reported package-lock/package.json inconsistency.

### Root Cause

Frontend dependencies had changed without committing the updated package-lock.

### Affected Job

Frontend CI

### Solution

Updated and committed `package.json` and `package-lock.json` together.

### Final Behaviour

`npm ci` installs reproducibly.

---

## Example Issue — Frontend Lint Command Did Not Exist

### Observed Behaviour

CI returned:

```text
Missing script: lint
```

### Root Cause

The earlier frontend contained only development/build scripts.

### Affected Job

Frontend CI

### Solution

Added ESLint and the `lint` script.

### Final Behaviour

Frontend lint executes in CI.

---

## Example Issue — AI Test Attempted a Real Provider Call

### Observed Behaviour

An automated test attempted to initialize the live AI provider.

### Root Cause

The provider boundary was not mocked.

### Affected Job

Backend CI

### Solution

Patched the `LLMService` dependency in the AI unit test.

### Final Behaviour

AI application logic is tested deterministically without paid provider calls.
