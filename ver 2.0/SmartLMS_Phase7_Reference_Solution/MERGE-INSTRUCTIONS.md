# Phase 7 Merge Instructions

This package is a **Phase 7 overlay** for the existing working Phase 6 SmartLMS repository.

## Copy directly

These files can normally be copied into the repository root/paths:

- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `backend/Dockerfile`
- `backend/.dockerignore`
- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `docs/docker-setup.md`
- `docs/phase7-docker-test-plan.md`
- `docs/phase7-docker-notes.md`

## Merge rather than blindly replace

`README.md` in this package contains the Phase 7 reference README update. If the Phase 6 repository already has a comprehensive README, merge the Docker/Phase 7 sections into it instead of deleting earlier documentation.

## Existing Phase 6 code that must remain

Do not delete the existing:

- React source tree
- Flask source tree
- SQLAlchemy models
- Alembic/Flask-Migrate migrations
- Phase 6 AI modules
- pgvector migration
- AI Quiz Generator
- RAG Tutor
- CourseChunk model
- tests and earlier documentation

## Before running

The existing frontend should have a committed `package-lock.json` because the reference frontend Dockerfile uses `npm ci`.

The existing backend should include all Phase 6 Python dependencies in `backend/requirements.txt`.

## First run

```bash
cp .env.example .env
# edit .env

docker compose build
docker compose up -d
docker compose exec backend flask --app run.py db upgrade
docker compose ps
```

Then execute `docs/phase7-docker-test-plan.md`.
