# SmartLMS — Phase 9 Submission Checklist

## Repository Files

Submit the existing SmartLMS project with the Phase 9 additions:

```text
ai-powered-lms/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml          # if advanced CD implemented
│
├── backend/
│   ├── requirements-ci.txt
│   ├── ruff.toml
│   ├── tests/
│   └── ...
│
├── frontend/
│   ├── eslint.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── src/test/
│   └── ...
│
├── docs/
│   ├── cicd-design.md
│   ├── phase9-cicd-test-plan.md
│   ├── phase9-cicd-notes.md
│   ├── phase9-security-checklist.md
│   └── phase9-rollback.md       # advanced
│
└── README.md
```

## Required Evidence

- [ ] Successful GitHub Actions run.
- [ ] Failed → Fixed → Passed pipeline example.
- [ ] Pull Request showing CI checks.

## Advanced Evidence

If advanced CD is implemented:

- [ ] Docker image build.
- [ ] Image push.
- [ ] Deployment.
- [ ] Health check.

## Do Not Submit

Never submit:

- `.env`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- production `DATABASE_URL`
- database password
- production `JWT_SECRET_KEY`
- private SSH keys
- `.pem` files
- real GitHub secret values
