# Phase 9 — CI/CD

SmartLMS uses GitHub Actions for Continuous Integration.

Workflow:

```text
.github/workflows/ci.yml
```

The workflow runs on pushes and pull requests targeting the approved `main` and `develop` branches.

## Backend CI

Backend validation performs:

1. Python 3.12 setup.
2. Dependency installation.
3. Disposable PostgreSQL/pgvector setup.
4. Ruff lint/static checks.
5. pytest.

The CI database is isolated and is never the production RDS database.

## Frontend CI

Frontend validation performs:

1. Node.js 22 setup.
2. `npm ci`.
3. ESLint.
4. Vitest.
5. `npm run build`.

## AI Testing

Automated AI tests mock the provider boundary.

CI does not repeatedly call the real paid AI service.

## Failure Behaviour

Any mandatory lint, test, or build failure causes GitHub Actions to fail.

## Secrets

Production credentials are not stored in workflow YAML.

The mandatory CI workflow does not require production AWS, RDS, JWT, or AI credentials.

## Advanced CD

Where enabled:

```text
CI Pass
↓
Build Backend Docker Image
↓
Push Image to Registry
↓
Deploy Backend
↓
Deploy Frontend
↓
Production Health Check
```

See:

```text
docs/cicd-design.md
```

## Project Status

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Product Discovery | Complete |
| Phase 2 | Architecture & Database Design | Complete |
| Phase 3 | Backend Development | Complete |
| Phase 4 | React Frontend | Complete |
| Phase 5 | Full-Stack Integration | Complete |
| Phase 6 | AI / Agentic System | Complete |
| Phase 7 | Dockerisation | Complete |
| Phase 8 | Cloud Deployment | Complete |
| Phase 9 | CI/CD | Complete after pipeline verification |
| Phase 10 | Testing & Hardening | Next |
