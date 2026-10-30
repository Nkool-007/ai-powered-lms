# Phase 9 Merge Instructions

This package is intended to be merged into the **working Phase 8 SmartLMS repository**.

## 1. Copy Directly

These files can normally be copied into the repository as new files:

```text
.github/workflows/ci.yml
.github/workflows/deploy.yml              # Advanced / optional
backend/requirements-ci.txt
backend/ruff.toml
backend/tests/test_ai_ci.py
frontend/eslint.config.js
frontend/src/test/setup.js
frontend/src/test/ci-smoke.test.jsx
docs/cicd-design.md
docs/phase9-cicd-test-plan.md
docs/phase9-cicd-notes.md
docs/phase9-security-checklist.md
docs/phase9-rollback.md
docs/phase9-review-demo.md
docs/phase9-viva-questions.md
docs/phase9-definition-of-done.md
docs/phase9-submission-checklist.md
docs/phase9-github-settings.md
```

## 2. Merge — Do Not Blindly Replace

### `backend/tests/conftest.py`

Use:

```text
backend/tests/conftest.phase9-reference.py
```

as the reference and preserve all fixtures already needed by the existing test suite.

The key Phase 9 requirement is that the test fixture continues to respect:

```text
TEST_DATABASE_URL
```

and never uses the production RDS database.

### `frontend/package.json`

Use:

```text
frontend/package.phase9-reference.json
```

as the reference for the new scripts and devDependencies.

Preserve all existing dependencies added during Phases 4–8.

### `frontend/vite.config.js`

Use:

```text
frontend/vite.config.phase9-reference.js
```

as the reference.

Keep the existing Vite configuration and merge the `test` block.

### Root `README.md`

Use:

```text
README-PHASE9-SECTION.md
```

and merge that section into the existing project README.

### `.gitignore`

Use:

```text
.gitignore.phase9-snippet
```

only as a review checklist. Preserve the existing `.gitignore`.

## 3. `package-lock.json`

Do not fabricate a lock file.

After merging the Phase 9 `package.json` dependencies into the actual Phase 8 frontend:

```bash
cd frontend
npm install
```

Commit the resulting:

```text
package.json
package-lock.json
```

together.

CI then uses:

```bash
npm ci
```

## 4. Validate Locally Before Pushing

Backend:

```bash
cd backend
pip install -r requirements-ci.txt
ruff check app tests run.py
pytest -q
```

Frontend:

```bash
cd frontend
npm install
npm run lint
npm run test
npm run build
```

## 5. CI Database

The reference `ci.yml` starts a disposable:

```text
PostgreSQL + pgvector
```

service and creates the `vector` extension.

It never connects to production RDS.

## 6. AI Tests

CI must not repeatedly call the real paid AI provider.

The supplied:

```text
backend/tests/test_ai_ci.py
```

patches the `LLMService` provider boundary.

## 7. Advanced Deployment

`deploy.yml` is optional and assumes:

- Phase 8 manual deployment already works.
- Amazon ECR exists.
- EC2 is managed by AWS Systems Manager.
- EC2 can pull ECR images.
- A production environment file already exists on EC2.
- GitHub-to-AWS OIDC or another approved credential mechanism is configured.

Do not enable the advanced workflow until manual production deployment is stable.
