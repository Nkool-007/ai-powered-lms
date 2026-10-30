# SmartLMS — Cloud Deployment Guide

## 1. Deployment Architecture

Production SmartLMS uses:

- Frontend: Amazon S3 + CloudFront
- Backend: Amazon EC2 + Docker + Gunicorn + Flask
- Database: Amazon RDS PostgreSQL
- Vector Store: PostgreSQL + pgvector
- AI: External provider accessed only by Flask

## 2. AWS Region

Selected Region:

`<SELECTED_AWS_REGION>`

The exact deployment region must be recorded by the deployment team.

## 3. Frontend Deployment

### Build

```bash
cd frontend
npm ci
npm run build
```

Production output:

```text
frontend/dist/
```

### Upload

```bash
aws s3 sync frontend/dist/ s3://<FRONTEND_BUCKET>/ --delete
```

### CloudFront

Serve the S3 origin through CloudFront.

Use HTTPS for browser access.

### Frontend URL

```text
https://<FRONTEND_CLOUDFRONT_DOMAIN>
```

### API Configuration

The React production build uses:

```text
VITE_API_BASE_URL=https://<PUBLIC_API_HOST>/api/v1
```

The production frontend must never call localhost.

### Cache Invalidation

After deploying a changed build, invalidate stale CloudFront paths where required:

```bash
aws cloudfront create-invalidation \
  --distribution-id <FRONTEND_DISTRIBUTION_ID> \
  --paths "/*"
```

### React SPA Routing

Verify that direct navigation and refresh work for routes such as:

- `/`
- `/login`
- `/student/dashboard`
- one `/courses/...` route

Use an approved SPA routing configuration so React Router receives the route through `index.html`.

## 4. Backend Deployment

The backend is deployed to EC2 using Docker.

Production image:

```text
smartlms-backend:phase8
```

Build:

```bash
docker build \
  -f backend/Dockerfile.prod \
  -t smartlms-backend:phase8 \
  ./backend
```

Run:

```bash
docker run -d \
  --name smartlms-backend \
  --restart unless-stopped \
  --env-file /opt/smartlms/backend.env \
  -p 80:8000 \
  smartlms-backend:phase8
```

Gunicorn serves Flask inside the container.

Restart:

```bash
docker restart smartlms-backend
```

Inspect:

```bash
docker ps
```

Logs:

```bash
docker logs -f --tail 100 smartlms-backend
```

Public API:

```text
https://<PUBLIC_API_HOST>/api/v1
```

## 5. Database Deployment

Production database:

Amazon RDS PostgreSQL

Database name:

```text
ai_powered_lms
```

Connection is supplied through:

```text
DATABASE_URL
```

The backend does not use `localhost` or `postgres` as the production database hostname.

It uses the actual RDS endpoint.

RDS should not be publicly accessible to arbitrary clients.

## 6. Database Migrations

Run:

```bash
docker exec smartlms-backend \
  flask --app run.py db upgrade
```

Verify:

```bash
docker exec smartlms-backend \
  flask --app run.py db current
```

Tables are created through migration history, not manual recreation.

## 7. pgvector

Verify the vector extension where required:

```sql
SELECT extname
FROM pg_extension
WHERE extname = 'vector';
```

Verify indexed chunks:

```sql
SELECT COUNT(*)
FROM course_chunks;
```

The production AI Tutor is not considered working until vector storage and retrieval work in RDS.

## 8. AI Configuration

Backend variable names:

- `LLM_PROVIDER`
- `OPENAI_API_KEY`
- `LLM_MODEL`
- `EMBEDDING_MODEL`
- `VECTOR_STORE_TYPE`
- `AI_REQUEST_TIMEOUT_SECONDS`
- `RAG_TOP_K`
- `RAG_MAX_COSINE_DISTANCE`
- `RAG_CHUNK_WORDS`
- `RAG_CHUNK_OVERLAP_WORDS`

Do not store secret values in this document.

## 9. CORS

Production frontend:

```text
https://<FRONTEND_CLOUDFRONT_DOMAIN>
```

Backend variable:

```text
FRONTEND_ORIGIN=https://<FRONTEND_CLOUDFRONT_DOMAIN>
```

Localhost should not remain the only production origin.

## 10. HTTPS

Frontend access uses CloudFront HTTPS.

The public API should also be exposed through an approved HTTPS endpoint.

Target:

```text
Browser
  ↓ HTTPS
Frontend
  ↓ HTTPS
Backend
```

## 11. Public URLs

Frontend:

```text
https://<FRONTEND_CLOUDFRONT_DOMAIN>
```

Backend:

```text
https://<PUBLIC_API_HOST>
```

API Base:

```text
https://<PUBLIC_API_HOST>/api/v1
```

Health:

```text
https://<PUBLIC_API_HOST>/api/v1/health
```

Replace placeholders only after deployment.

## 12. Logs

Backend logs:

```bash
docker logs smartlms-backend
```

Follow:

```bash
docker logs -f --tail 100 smartlms-backend
```

Logs should help diagnose:
- startup failures
- database failures
- authentication errors
- application exceptions
- AI failures
- migration failures

Secrets must never be logged.

## 13. Deploying a New Frontend Version

1. Pull the approved source.
2. Configure the production API URL.
3. Run `npm ci`.
4. Run `npm run build`.
5. Sync `dist/` to S3.
6. Invalidate CloudFront cache where required.
7. Run smoke tests.

## 14. Deploying a New Backend Version

1. Pull approved source.
2. Build new Docker image.
3. Stop the old container.
4. Start the new container with the production environment file.
5. Apply migrations when required.
6. Check health endpoint.
7. Review logs.
8. Run application smoke tests.

## 15. Troubleshooting

### Frontend still calls localhost

Cause: Production `VITE_API_BASE_URL` was incorrect when React was built.

Solution: rebuild React using the production API URL and redeploy `dist/`.

### CORS error

Check `FRONTEND_ORIGIN`.

It must match the actual browser frontend origin.

### Backend cannot connect to RDS

Check:
- `DATABASE_URL`
- RDS endpoint
- database security group
- backend security group
- database credentials

### Tables missing

Run:

```bash
flask --app run.py db upgrade
```

inside the production backend environment.

### RAG fails

Check:
- pgvector support
- `course_chunks` table
- embedding provider
- course reindex
- `course_id` filtering

### AI fails while core LMS works

Check backend AI environment variables and backend logs.

This is a controlled partial-service failure.

### CloudFront serves old frontend

Redeploy the current build and invalidate outdated cache entries.
