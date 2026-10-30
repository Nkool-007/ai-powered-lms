# SmartLMS — Phase 9 Review Demo

## Part 1 — Explain CI/CD

Explain:

```text
Developer
↓
GitHub
↓
GitHub Actions
↓
Automated Validation
```

Then explain the difference between CI and CD.

## Part 2 — Show Workflow File

Open:

```text
.github/workflows/ci.yml
```

Explain:

- trigger
- backend job
- frontend job
- test database
- lint
- tests
- build

## Part 3 — Show Successful Run

Show:

```text
Backend CI   ✓
Frontend CI  ✓
```

## Part 4 — Show Failed Run

Show one real previous failing workflow.

Explain:

- What failed?
- Why did it fail?
- How was it fixed?

## Part 5 — Backend CI

Explain:

```text
Python
↓
Dependencies
↓
PostgreSQL/pgvector
↓
Ruff
↓
pytest
```

## Part 6 — Frontend CI

Explain:

```text
Node
↓
npm ci
↓
ESLint
↓
Vitest
↓
Vite Build
```

## Part 7 — AI Testing Safety

Show the mocked `LLMService`.

Explain why CI does not repeatedly call the paid provider.

## Part 8 — Secrets

Show workflow YAML and prove that no real AWS secret, production database password, JWT secret, or AI provider key is hard-coded.

## Part 9 — Advanced CD

If implemented, show:

```text
CI PASS
↓
ECR
↓
EC2
↓
S3 / CloudFront
↓
Health Check
```
