# EDUZZA SmartLMS

## AI-Powered Learning Management System

This file contains the Phase 7 reference README update. When applying this package to an existing Phase 6 repository, retain the project's earlier README content and merge the sections below rather than discarding project-specific documentation.

## Current Project Status

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Product Discovery & Requirements | Complete |
| Phase 2 | Architecture & Database Design | Complete |
| Phase 3 | Flask Backend | Complete |
| Phase 4 | React Frontend | Complete |
| Phase 5 | Full-Stack Integration | Complete |
| Phase 6 | AI / Agentic System | Complete |
| Phase 7 | DevOps Foundation & Dockerisation | Complete |
| Next | Cloud Deployment | Pending |

## Phase 7 Architecture

```text
Browser
  |
  +--> React / Vite container
  |      http://localhost:5173
  |
  +--> Flask REST API container
         http://localhost:5000
             |
             v
        PostgreSQL + pgvector
             |
             v
      smartlms_postgres_data
```

The LLM/Embedding Provider remains external and is called only from the Flask backend.

## Docker Services

- `frontend` - React + Vite
- `backend` - Flask REST API
- `postgres` - PostgreSQL + pgvector

## Prerequisites

- Git
- Docker
- Docker Compose
- Approved AI Provider credentials for Phase 6 AI features

## Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and provide the required credentials.

Never commit the real `.env`.

## Build

```bash
docker compose build
```

## Start

```bash
docker compose up -d
```

## Apply Database Migrations

```bash
docker compose exec backend \
  flask --app run.py db upgrade
```

## Check Containers

```bash
docker compose ps
```

Expected concept:

```text
frontend -> running / healthy
backend  -> running / healthy
postgres -> running / healthy
```

## Application URLs

| Component | Address |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:5000` |
| API Base | `http://localhost:5000/api/v1` |
| Health | `http://localhost:5000/api/v1/health` |
| PostgreSQL from Backend | `postgres:5432` |

## Database Persistence

PostgreSQL uses the Docker named volume:

```text
smartlms_postgres_data
```

Normal shutdown preserves this volume:

```bash
docker compose down
```

Do not use `docker compose down -v` unless intentional database deletion is required.

## View Logs

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
```

Follow backend logs:

```bash
docker compose logs -f backend
```

## AI / RAG Verification

After Dockerisation, verify that the Phase 6 capabilities still work:

- AI Quiz Generator
- Instructor human review before saving AI-generated Quiz content
- Course re-indexing
- Embedding persistence
- PostgreSQL/pgvector retrieval
- `course_id` isolation
- Course-Aware AI Tutor
- Tutor citations
- AI conversation persistence
- Controlled AI failures

AI credentials remain backend-only. The frontend must never receive `OPENAI_API_KEY`, `JWT_SECRET_KEY`, or database credentials.

## Security Principles

- Real `.env` is never committed.
- Secrets are not hard-coded in Dockerfiles.
- `.dockerignore` excludes `.env`.
- `.gitignore` excludes `.env`.
- PostgreSQL is not unnecessarily exposed through a host port.
- Browser-facing configuration may use `VITE_*`; backend secrets must not.

## Phase 7 Result

SmartLMS can now be started as a reproducible containerized environment without requiring local PostgreSQL, local Python dependencies, or local frontend Node dependencies on the host.

The next project phase is Cloud Deployment.
