# SmartLMS - Docker Setup Guide

## 1. Purpose

SmartLMS uses Docker Compose to run its development application stack consistently.

The containerized services are:

- `frontend` - React + Vite
- `backend` - Flask REST API
- `postgres` - PostgreSQL + pgvector

The LLM/Embedding Provider remains an external managed service.

## 2. Architecture

```text
Browser
  |
  +-- http://localhost:5173
  |        |
  |        v
  |     React/Vite
  |
  +-- http://localhost:5000
           |
           v
        Flask API
           |
           v
      postgres:5432
           |
           v
   PostgreSQL + pgvector
```

## 3. Prerequisites

Required on the host:

- Git
- Docker
- Docker Compose

Required external configuration:

- LLM / Embedding Provider credential

Node.js, Python, and PostgreSQL do not need to be installed locally to run the Dockerized stack.

## 4. Environment Configuration

Copy the template:

```bash
cp .env.example .env
```

Edit `.env` and configure at minimum:

- `POSTGRES_PASSWORD`
- `JWT_SECRET_KEY`
- `OPENAI_API_KEY`
- `LLM_MODEL`
- `EMBEDDING_MODEL`

Never commit `.env`.

## 5. Build

```bash
docker compose build
```

## 6. Start

```bash
docker compose up -d
```

Inspect status:

```bash
docker compose ps
```

## 7. Database Migration

```bash
docker compose exec backend \
  flask --app run.py db upgrade
```

Docker does not replace Alembic/Flask-Migrate. Schema history remains migration-driven.

## 8. Application URLs

| Component | Address |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:5000` |
| API Base | `http://localhost:5000/api/v1` |
| Health | `http://localhost:5000/api/v1/health` |
| PostgreSQL from Backend | `postgres:5432` |
| PostgreSQL Database | `ai_powered_lms` |

### Browser vs Docker-internal networking

Browser-facing API calls use:

```text
http://localhost:5000/api/v1
```

The Flask backend connects to PostgreSQL using Docker DNS:

```text
postgres:5432
```

Inside the backend container, `localhost` refers to the backend container itself, not PostgreSQL.

## 9. Shutdown

```bash
docker compose down
```

Normal shutdown preserves the PostgreSQL named volume.

Do not use the following during normal shutdown unless database deletion is intentional:

```bash
docker compose down -v
```

## 10. Rebuild

After Dockerfile or dependency changes:

```bash
docker compose up -d --build
```

## 11. View Logs

Backend:

```bash
docker compose logs backend
```

Frontend:

```bash
docker compose logs frontend
```

PostgreSQL:

```bash
docker compose logs postgres
```

Follow backend logs:

```bash
docker compose logs -f backend
```

## 12. Open PostgreSQL Shell

```bash
docker compose exec postgres \
  psql \
  -U smartlms \
  -d ai_powered_lms
```

## 13. Verify pgvector

Inside PostgreSQL:

```sql
SELECT extname
FROM pg_extension
WHERE extname = 'vector';
```

Expected result:

```text
vector
```

## 14. Verify Course Chunks

After Course re-indexing:

```bash
docker compose exec postgres \
  psql \
  -U smartlms \
  -d ai_powered_lms \
  -c "SELECT COUNT(*) FROM course_chunks;"
```

Expected: count greater than zero for an indexed Course.

## 15. Troubleshooting - Port Already in Use

Typical symptoms:

```text
Bind for 0.0.0.0:5173 failed
```

or:

```text
Bind for 0.0.0.0:5000 failed
```

Stop the conflicting process or change `FRONTEND_PORT` / `BACKEND_PORT` in `.env`.

If the frontend host port changes, also update `FRONTEND_ORIGIN` accordingly.

## 16. Troubleshooting - Backend Cannot Reach PostgreSQL

Check service state:

```bash
docker compose ps
```

Check PostgreSQL logs:

```bash
docker compose logs postgres
```

Verify `DATABASE_URL` contains:

```text
@postgres:5432
```

not:

```text
@localhost:5432
```

## 17. Troubleshooting - Migration Missing

A typical symptom is:

```text
relation "users" does not exist
```

Run:

```bash
docker compose exec backend \
  flask --app run.py db upgrade
```

## 18. Troubleshooting - pgvector Missing

Check installed PostgreSQL extensions:

```sql
SELECT extname
FROM pg_extension;
```

Confirm the PostgreSQL image supports pgvector and the Phase 6 migration enabling:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

has run.

## 19. Troubleshooting - Frontend Cannot Reach Backend

Check:

```text
VITE_API_BASE_URL
```

Expected local Docker development value:

```text
http://localhost:5000/api/v1
```

Browser JavaScript normally cannot resolve the Docker service name `backend`.

## 20. Troubleshooting - CORS

Verify:

```text
FRONTEND_ORIGIN=http://localhost:5173
```

Restart the backend if required:

```bash
docker compose restart backend
```

## 21. Troubleshooting - AI Provider Error

Check:

- `OPENAI_API_KEY`
- `LLM_MODEL`
- `EMBEDDING_MODEL`

Inspect backend logs:

```bash
docker compose logs backend
```

Core LMS functionality should remain operational even when AI is unavailable.
