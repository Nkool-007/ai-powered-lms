# Phase 7 Docker Security Review

Use this checklist before marking Phase 7 complete.

- [ ] No API keys inside the frontend Dockerfile.
- [ ] No API keys inside the backend Dockerfile.
- [ ] No database passwords inside Dockerfiles.
- [ ] No JWT secrets inside Dockerfiles.
- [ ] Real `.env` is ignored by Git.
- [ ] `.env.example` contains placeholders only.
- [ ] `OPENAI_API_KEY` is supplied only to the backend.
- [ ] Frontend receives no backend secret.
- [ ] Database password is runtime configuration.
- [ ] PostgreSQL has no unnecessary published host port.
- [ ] Database remains accessible to backend through the internal Docker network.
- [ ] Docker images do not intentionally bake local `.env` files.
- [ ] `.dockerignore` excludes `.env`.
- [ ] `.gitignore` excludes `.env`.
- [ ] Core LMS remains operational if the AI provider fails.

## Verify no real `.env` is tracked

```bash
git ls-files | grep -E '(^|/)\.env$'
```

Expected: no output.

## Search repository for common secret variable names

```bash
git grep -n -E 'OPENAI_API_KEY|JWT_SECRET_KEY|DATABASE_PASSWORD'
```

References to variable names are acceptable. Real secret values must not be present in committed files.

## Important Principle

```text
Environment Variable
!=
Automatically Secure
```

Do not print secrets in logs, return secrets through APIs, place backend secrets into `VITE_*`, commit the runtime `.env`, or paste credentials into documentation.
