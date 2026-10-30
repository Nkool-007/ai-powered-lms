# SmartLMS — Phase 9 Definition of Done

## Repository

- [ ] `.github/workflows/` exists.
- [ ] `ci.yml` exists.
- [ ] CI YAML is committed.
- [ ] CI documentation exists.

## Triggering

- [ ] CI runs on approved pushes.
- [ ] CI runs on Pull Requests.
- [ ] Workflow runs automatically.

## Backend

- [ ] Python environment is created automatically.
- [ ] Dependencies install automatically.
- [ ] Disposable test database works.
- [ ] pgvector test environment works.
- [ ] Ruff executes.
- [ ] pytest executes.
- [ ] Failed backend test fails CI.

## Frontend

- [ ] Node environment is created automatically.
- [ ] `npm ci` succeeds.
- [ ] ESLint executes.
- [ ] Vitest executes.
- [ ] Production build executes.
- [ ] Failed frontend check fails CI.

## AI

- [ ] CI does not depend unnecessarily on a live paid AI provider.
- [ ] AI provider behaviour can be mocked.
- [ ] Production AI credentials are not committed.

## Security

- [ ] No AWS secret is hard-coded.
- [ ] No production database password is hard-coded.
- [ ] No production JWT secret is hard-coded.
- [ ] No production AI key is hard-coded.
- [ ] CI permissions are reviewed.
- [ ] Test configuration is isolated from production.

## Verification

- [ ] Successful workflow run demonstrated.
- [ ] Failed workflow run demonstrated.
- [ ] Fix demonstrated.
- [ ] Final passing workflow demonstrated.
- [ ] Pull Request displays CI status.

## Documentation

- [ ] `docs/cicd-design.md`
- [ ] `docs/phase9-cicd-test-plan.md`
- [ ] `docs/phase9-cicd-notes.md`
- [ ] CI/CD README section
- [ ] Workflow behaviour is explainable.

## Advanced CD — If Implemented

- [ ] Docker image builds only after successful CI.
- [ ] Image is pushed to an approved registry.
- [ ] Image is traceable to commit SHA.
- [ ] Deployment occurs only for approved `main` code.
- [ ] Backend deployment is automated.
- [ ] Frontend deployment is automated.
- [ ] CloudFront invalidation works.
- [ ] Production health check runs.
- [ ] Credentials use approved secret/identity handling.
- [ ] Rollback process is documented.
