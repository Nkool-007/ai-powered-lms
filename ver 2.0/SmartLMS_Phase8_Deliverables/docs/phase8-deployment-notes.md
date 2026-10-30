# SmartLMS — Phase 8 Deployment Notes

> Students should keep only issues actually encountered during their deployment. The entries below are reference examples.

---

## Issue 1 — Production Frontend Called localhost

### Observed Behaviour
The CloudFront website loaded but API requests attempted to access:

`http://localhost:5000/api/v1`

### Root Cause
The React build was created using the development `VITE_API_BASE_URL`.

### Affected Layer
Frontend → Backend Integration

### Solution
Configured the production API URL before running `npm run build`, then rebuilt and redeployed `dist/`.

### Final Behaviour
The deployed React application sends API requests to the cloud backend.

---

## Issue 2 — EC2 Could Not Connect to RDS

### Observed Behaviour
Backend database operations returned connection errors.

### Root Cause
The RDS security configuration did not permit PostgreSQL traffic from the backend security group.

### Affected Layer
EC2 → RDS Networking

### Solution
Allowed PostgreSQL port 5432 from the backend security group to the database security group.

### Final Behaviour
Flask connects successfully to RDS.

---

## Issue 3 — Production Tables Were Missing

### Observed Behaviour
API requests failed with missing-table errors.

### Root Cause
RDS was created successfully, but migration history had not yet been applied.

### Affected Layer
Database Schema

### Solution

```bash
docker exec smartlms-backend flask --app run.py db upgrade
```

### Final Behaviour
The RDS database contains the current SmartLMS schema.

---

## Issue 4 — Production CORS Failure

### Observed Behaviour
The browser blocked API requests.

### Root Cause
`FRONTEND_ORIGIN` still used `http://localhost:5173`.

### Affected Layer
Browser / Flask CORS

### Solution
Configured `FRONTEND_ORIGIN` using the actual production frontend origin and restarted the backend.

### Final Behaviour
The CloudFront frontend can access the Flask API.

---

## Issue 5 — AI Worked Locally but Not on EC2

### Observed Behaviour
Core LMS endpoints worked, while AI endpoints returned an AI configuration error.

### Root Cause
The AI provider credential was missing from the production backend environment.

### Affected Layer
Flask → AI Provider

### Solution
Configured the backend-only AI environment variables and restarted the container.

### Final Behaviour
AI Quiz generation and Tutor requests work in production.

---

## Issue 6 — RAG Returned No Results

### Observed Behaviour
AI Tutor reported insufficient Course context after deployment.

### Root Cause
The Course had not been re-indexed against the production vector store.

### Affected Layer
RAG / Vector Store

### Solution
Ran the production Course re-index workflow.

### Final Behaviour
Course chunks and embeddings exist in RDS and retrieval succeeds.

---

## Issue 7 — CloudFront Served an Old Frontend

### Observed Behaviour
A new build was uploaded to S3 but users continued receiving old JavaScript.

### Root Cause
Cached CloudFront assets were still active.

### Affected Layer
Frontend Delivery

### Solution
Invalidated the required CloudFront paths after deployment.

### Final Behaviour
Users receive the new frontend version.
