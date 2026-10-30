# EDUZZA SmartLMS — Phase 9 Reference Solution

## Phase 9 — CI/CD with GitHub Actions

This package is a **Phase 9 reference-solution overlay** for the existing SmartLMS project completed through Phase 8.

It demonstrates the expected engineering standard for:

- GitHub Actions CI
- push / pull-request triggers
- backend dependency installation
- Ruff linting
- pytest execution
- disposable PostgreSQL + pgvector testing
- frontend dependency installation with `npm ci`
- ESLint
- Vitest + React Testing Library
- Vite production build verification
- CI failure behaviour
- AI-safe mocked testing
- secret/permission review
- CI/CD documentation
- optional advanced Docker/ECR/EC2/S3/CloudFront deployment
- production health gates
- rollback design

## Important

Do **not** blindly replace the completed Phase 8 repository with this folder.

Use `MERGE-INSTRUCTIONS.md`.

Several files are intentionally supplied as merge references because the real Phase 8 repository may already contain settings that must remain.

## Mandatory vs Advanced

### Mandatory Phase 9

- `.github/workflows/ci.yml`
- backend CI dependencies and Ruff configuration
- backend tests executed in CI
- frontend lint/test/build configuration
- AI provider mocking strategy
- CI/CD documentation
- failure demonstration
- successful workflow evidence
- security and permissions review

### Advanced / Optional

- `.github/workflows/deploy.yml`
- Docker image push to Amazon ECR
- EC2 deployment through AWS Systems Manager
- S3 frontend deployment
- CloudFront invalidation
- post-deployment health gate
- rollback design

## Phase Boundary

Phase 9 establishes the automation pipeline.

Phase 10 expands the complete Testing & Hardening strategy.
