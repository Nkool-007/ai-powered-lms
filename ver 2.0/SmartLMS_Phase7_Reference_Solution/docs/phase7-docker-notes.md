# SmartLMS - Phase 7 Docker Integration Notes

This document records reference integration issues while moving the Phase 6 SmartLMS application into Docker.

> Students should document the actual problems found in their own implementation rather than claiming issues they did not encounter.

## Issue 1 - Backend Could Not Connect to PostgreSQL

### Observed Behaviour

The Flask container started but database requests failed.

### Root Cause

The previous local development `DATABASE_URL` used `localhost:5432`. Inside the backend container, `localhost` refers to the backend container itself.

### Affected Layer

Backend -> Database Networking

### Solution

Changed the Docker database URL to use the Compose service hostname:

```text
postgres:5432
```

### Final Behaviour

The Flask backend successfully connects to PostgreSQL through the Docker network.

---

## Issue 2 - Backend Started Before PostgreSQL Was Ready

### Observed Behaviour

The backend occasionally failed during startup on a fresh environment.

### Root Cause

Container startup order did not guarantee that PostgreSQL was ready to accept connections.

### Affected Layer

Docker Compose Service Startup

### Solution

Added a PostgreSQL health check using `pg_isready` and configured:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

### Final Behaviour

The backend starts only after PostgreSQL reports a healthy state.

---

## Issue 3 - Browser Could Not Reach `backend:5000`

### Observed Behaviour

React loaded successfully but API requests failed.

### Root Cause

`VITE_API_BASE_URL` was configured as:

```text
http://backend:5000/api/v1
```

The Docker service name `backend` is resolvable between containers but not from the user's browser.

### Affected Layer

Frontend -> Backend Networking

### Solution

Configured the browser-facing API URL as:

```text
http://localhost:5000/api/v1
```

### Final Behaviour

The browser reaches Flask through the backend's published host port.

---

## Issue 4 - CORS Rejected Frontend Requests

### Observed Behaviour

The browser reported CORS errors despite Flask being reachable.

### Root Cause

`FRONTEND_ORIGIN` did not match the actual browser origin.

### Affected Layer

Browser / Flask CORS

### Solution

Configured:

```text
FRONTEND_ORIGIN=http://localhost:5173
```

### Final Behaviour

Requests from the local Dockerized frontend are accepted while CORS remains explicitly restricted.

---

## Issue 5 - Database Tables Were Missing

### Observed Behaviour

The application started, but API requests returned database errors indicating missing tables.

### Root Cause

Docker started PostgreSQL with a fresh empty volume, but Alembic migrations had not yet run.

### Affected Layer

Database Schema

### Solution

Executed:

```bash
docker compose exec backend flask --app run.py db upgrade
```

### Final Behaviour

The complete migration history is applied to fresh databases.

---

## Issue 6 - pgvector Extension Was Missing

### Observed Behaviour

`CourseChunk` migration or vector operations failed.

### Root Cause

The PostgreSQL runtime did not initially contain the vector extension.

### Affected Layer

Phase 6 RAG / PostgreSQL

### Solution

Used a PostgreSQL image containing pgvector support and retained the Phase 6 migration:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Final Behaviour

Embeddings can be persisted and cosine-distance retrieval functions correctly.

---

## Issue 7 - AI Provider Credential Was Missing

### Observed Behaviour

Core LMS routes worked, but the AI Quiz Generator and AI Tutor returned controlled AI configuration errors.

### Root Cause

`OPENAI_API_KEY` was not provided to the backend container.

### Affected Layer

External AI Integration

### Solution

Added the key to the local `.env` and restarted the backend container.

### Final Behaviour

AI functions work while the secret remains outside Git and outside the frontend image.
