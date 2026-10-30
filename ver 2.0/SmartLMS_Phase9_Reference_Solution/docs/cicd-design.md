# SmartLMS — CI/CD Design

## 1. Purpose

The purpose of CI/CD is to ensure that every important SmartLMS change can be validated consistently before it is merged or deployed.

CI should answer:

- Can backend dependencies install?
- Does backend code pass static checks?
- Do backend tests pass?
- Can frontend dependencies install?
- Does frontend code pass linting?
- Do frontend tests pass?
- Can React produce a production build?

The advanced CD workflow additionally answers:

- Can the production backend Docker image be built?
- Can it be stored in a registry?
- Can approved code be deployed?
- Is the application healthy after deployment?

## 2. Workflow Triggers

Mandatory CI runs on:

- Push to `main`.
- Push to `develop`.
- Pull Request targeting `main`.
- Pull Request targeting `develop`.

Feature branches therefore receive CI validation through their Pull Requests.

Production deployment is separated from Pull Request validation.

## 3. Mandatory CI Architecture

```text
Developer
↓
Git Push / Pull Request
↓
GitHub
↓
GitHub Actions
├── Backend CI
│   ├── Python
│   ├── Dependencies
│   ├── PostgreSQL + pgvector
│   ├── Ruff
│   └── pytest
│
└── Frontend CI
    ├── Node
    ├── npm ci
    ├── ESLint
    ├── Vitest
    └── Vite Production Build
```

If any mandatory step fails:

```text
CI = FAILED
```

No advanced deployment should proceed.

## 4. Backend CI Job

Backend CI uses Python 3.12.

It installs `backend/requirements-ci.txt`, which includes the normal application requirements plus the CI linter.

Checks:

1. Dependency installation.
2. PostgreSQL/pgvector availability.
3. Ruff lint/static check.
4. pytest.

## 5. Frontend CI Job

Frontend CI uses Node.js 22.

Steps:

1. `npm ci`
2. `npm run lint`
3. `npm run test`
4. `npm run build`

`npm ci` is used because `package-lock.json` is committed and therefore dependency resolution is reproducible.

## 6. Test Database

CI never connects to production RDS.

The reference workflow starts a disposable PostgreSQL + pgvector service inside the GitHub Actions job.

Reference configuration:

- Database: `smartlms_test`
- User: `smartlms_test`
- Password: CI-only disposable value

The database exists only for the workflow.

## 7. AI Test Strategy

CI does not repeatedly call a real paid LLM.

```text
Application AI Service
↓
Mocked Provider
↓
Application Logic
```

This permits deterministic tests for valid structured AI output, malformed output, provider failure, authorization, and retrieval behaviour without depending on an external paid provider.

## 8. Secrets

The mandatory CI workflow contains no production credentials.

It does not use:

- production RDS password
- production JWT signing key
- production OpenAI/Gemini key
- AWS secret keys

A harmless CI-only JWT value may be used.

Advanced deployment credentials use an approved GitHub/AWS credential mechanism.

## 9. Failure Rules

The workflow intentionally does not use `continue-on-error` for:

- lint
- backend tests
- frontend tests
- frontend build

A mandatory failure makes the workflow fail.

## 10. Deployment

The minimum Phase 9 solution may stop after successful CI.

The advanced solution continues:

```text
CI Pass
↓
Docker Build
↓
Container Registry
↓
Backend Deployment
↓
Frontend Deployment
↓
Health Verification
```

Deployment occurs only for approved `main` branch code.

## 11. Workflow Permissions

Mandatory CI uses:

```yaml
permissions:
  contents: read
```

because it only needs to read the repository.

Advanced deployment may additionally require:

```yaml
permissions:
  contents: read
  id-token: write
```

when AWS identity federation/OIDC is used.

The workflow receives only the permissions required by its job.

## 12. Known Limitations

The minimum CI implementation:

- does not provide full Phase 10 test coverage
- does not perform automatic rollback
- does not provide a separate staging environment
- does not perform penetration testing
- does not run expensive live-AI checks

Those areas belong to later testing/hardening or advanced deployment work.
