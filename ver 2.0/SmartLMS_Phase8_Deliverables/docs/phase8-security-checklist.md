# SmartLMS — Phase 8 Deployment Security Checklist

## Secrets

- [ ] No AWS secret keys committed.
- [ ] No AI provider keys committed.
- [ ] No database passwords committed.
- [ ] No JWT signing secret committed.
- [ ] Real `.env` files are ignored.
- [ ] README contains no credentials.
- [ ] Documentation contains no production passwords.

## Frontend

- [ ] React contains no backend secrets.
- [ ] No `VITE_*` variable contains a private credential.
- [ ] Production API URL points to cloud backend.
- [ ] HTTPS is used for public frontend.

## Backend

- [ ] JWT validation remains enabled.
- [ ] Role authorization remains backend-enforced.
- [ ] Instructor ownership checks remain active.
- [ ] Student enrollment checks remain active.
- [ ] Error responses do not expose stack traces/secrets.
- [ ] Logs do not contain credentials.

## Database

- [ ] RDS is not unnecessarily public.
- [ ] Database access is restricted to backend requirements.
- [ ] Database password is supplied at runtime.
- [ ] Migrations manage production schema.

## AI

- [ ] AI API key exists only on backend.
- [ ] AI cannot bypass authorization.
- [ ] Student must be enrolled before Tutor access.
- [ ] Retrieval remains filtered by `course_id`.
- [ ] AI Quiz Generator checks Instructor ownership.
- [ ] AI failure does not break the core LMS.

## Git

- [ ] `git status` contains no production secret.
- [ ] Private key files are not committed.
- [ ] `.env.example` contains placeholders only.
