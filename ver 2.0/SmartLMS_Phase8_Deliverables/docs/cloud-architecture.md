# SmartLMS — Production Cloud Architecture

## 1. Overview

SmartLMS is deployed on AWS using separated frontend, backend, database, and AI boundaries.

The production deployment contains:

1. React static frontend.
2. Flask REST backend.
3. PostgreSQL production database.
4. pgvector-based vector storage.
5. External AI provider.

## 2. Architecture

```text
Users
  ↓ HTTPS
CloudFront
  ↓
Amazon S3
  ↓
React Application
  ↓ HTTPS REST API
Public API Endpoint
  ↓
EC2
  ↓
Docker
  ↓
Gunicorn
  ↓
Flask
  ↓
RDS PostgreSQL

Flask
  ↓
External AI Provider

RDS PostgreSQL
  ↓
Relational LMS Data
+
Course Chunks
+
Embeddings
```

## 3. Frontend

Amazon S3 stores the compiled React production files.

Amazon CloudFront distributes those files to users.

The frontend contains:
- HTML
- JavaScript
- CSS
- static images

The frontend does not contain:
- database passwords
- JWT signing secrets
- AI API keys
- AWS secret keys

## 4. Backend

The Flask backend runs in a Docker container on EC2.

Responsibilities remain:
- Authentication
- Authorization
- Business rules
- Input validation
- Database access
- AI integration
- Course ownership
- Enrollment validation
- Quiz scoring
- Progress calculation
- RAG retrieval
- Error handling

The backend remains the authoritative application layer.

## 5. Database

Amazon RDS PostgreSQL stores:
- Users
- Courses
- Modules
- Lessons
- Enrollments
- Progress
- Quizzes
- Quiz attempts
- AI conversations
- AI messages
- Course chunks
- Vector embeddings

The reference Phase 8 deployment continues using PostgreSQL + pgvector.

## 6. AI

The AI provider remains external.

Correct:

```text
Browser
  ↓
React
  ↓
Flask
  ↓
AI Provider
```

Incorrect:

```text
Browser
  ↓
AI Provider Secret
```

## 7. Security Boundaries

- Frontend users can access public frontend assets.
- The public API can receive application requests.
- RDS is not intended to be directly accessible to public users.
- Only the backend requires database connectivity.
- Production secrets exist only in controlled backend/runtime configuration.

## 8. Environment Separation

Local:

```text
React → localhost Flask → Docker PostgreSQL
```

Production:

```text
CloudFront React → Cloud API → EC2 Flask → RDS PostgreSQL
```

Local Docker service names such as `postgres` must not be used as the RDS hostname.

## 9. Production Data Flow

```text
Student Request
  ↓
CloudFront Frontend
  ↓
HTTPS API
  ↓
Flask
  ↓
JWT Validation
  ↓
Authorization
  ↓
SQLAlchemy
  ↓
RDS
  ↓
JSON Response
  ↓
React
```

## 10. RAG Data Flow

```text
Student Question
  ↓
Cloud Frontend
  ↓
Flask
  ↓
Enrollment Check
  ↓
Query Embedding
  ↓
RDS pgvector Search
  ↓
course_id Filter
  ↓
Relevant Course Chunks
  ↓
AI Provider
  ↓
Answer + Sources
  ↓
Student
```

## 11. Failure Boundary

AI provider failure must not cause Login, Courses, Lessons, Enrollment, Progress, or Quiz functionality to stop working.

The AI service remains an enhancement to the core LMS.
