# SmartLMS — Phase 8 README Update

Use this content to update the project root `README.md`.

## Cloud Deployment

SmartLMS is designed for a production-style AWS architecture.

### Architecture

```text
Users
  ↓
CloudFront
  ↓
S3 React Frontend
  ↓
HTTPS API
  ↓
EC2 Flask Backend
  ↓
RDS PostgreSQL + pgvector

Flask
  ↓
External AI Provider
```

### Production Services

- Frontend Hosting: Amazon S3 + Amazon CloudFront
- Backend Hosting: Amazon EC2 + Docker + Gunicorn
- Database: Amazon RDS PostgreSQL
- Vector Store: PostgreSQL + pgvector
- AI: External AI Provider accessed through Flask

### Production URLs

Frontend:

```text
https://<FRONTEND_URL>
```

Backend:

```text
https://<BACKEND_URL>
```

API Base:

```text
https://<BACKEND_URL>/api/v1
```

Health:

```text
https://<BACKEND_URL>/api/v1/health
```

Replace placeholders with real deployment URLs only after deployment.

### Production Environment Variables

Backend variable names include:

```text
DATABASE_URL
JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES_HOURS
FRONTEND_ORIGIN
LLM_PROVIDER
OPENAI_API_KEY
LLM_MODEL
EMBEDDING_MODEL
VECTOR_STORE_TYPE
AI_REQUEST_TIMEOUT_SECONDS
RAG_TOP_K
RAG_MAX_COSINE_DISTANCE
RAG_CHUNK_WORDS
RAG_CHUNK_OVERLAP_WORDS
```

Actual secrets are not committed.

### Database Migrations

Production database migrations are applied using:

```bash
docker exec smartlms-backend \
  flask --app run.py db upgrade
```

Production tables are never manually recreated as a replacement for migration history.

### AI Deployment

The AI provider is accessed only by the Flask backend.

The browser never receives the AI provider credential.

The deployed application preserves:
- AI Quiz Generator
- Course re-indexing
- Course-scoped vector retrieval
- RAG Tutor
- Tutor citations
- Conversation persistence
- controlled AI failure handling

### Deployment Documentation

See:
- `docs/cloud-architecture.md`
- `docs/aws-resource-plan.md`
- `docs/cloud-deployment.md`
- `docs/phase8-deployment-test-plan.md`
- `docs/phase8-security-checklist.md`
- `docs/phase8-deployment-notes.md`
- `docs/phase8-urls.md`

## Project Status

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Product Discovery | Complete |
| Phase 2 | Architecture & Database Design | Complete |
| Phase 3 | Backend Development | Complete |
| Phase 4 | React Frontend | Complete |
| Phase 5 | Full-Stack Integration | Complete |
| Phase 6 | AI / Agentic System | Complete |
| Phase 7 | Dockerisation | Complete |
| Phase 8 | Cloud Deployment | Complete after production verification |
| Phase 9 | CI/CD | Next |

Do not mark Phase 8 complete before the actual AWS deployment passes the review gate.
