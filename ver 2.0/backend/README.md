# SmartLMS Backend — Phase 3 + Phase 5 Integrated Reference

This package implements the Flask/PostgreSQL backend defined in the Phase 3 reference
solution and includes the backend-side integration changes required by Phase 5.

## Included

- Flask REST API
- SQLAlchemy relational models
- PostgreSQL configuration
- Seven-step Alembic/Flask-Migrate baseline
- JWT authentication
- Student / Instructor / Admin RBAC
- Instructor course ownership
- Course / Module / Lesson APIs
- Enrollment and duplicate-enrollment protection
- Lesson completion and progress calculation
- Quiz creation, retrieval, discovery, submission and history
- Server-side quiz scoring
- Basic Admin APIs
- CORS for the approved React origin
- Standardized JWT / API errors
- ISO datetime serialization
- Automated pytest examples
- Postman demonstration guide

## Important Phase 5 Backend Additions

Phase 5 adds:

- `Flask-Cors`
- `FRONTEND_ORIGIN`
- standardized missing/invalid/expired/revoked JWT responses
- ISO datetime serialization
- course-level quiz discovery:
  `GET /api/v1/courses/{course_id}/quizzes`

React remains a UX layer. Flask remains authoritative for authentication, authorization,
ownership, enrollment and business rules.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Create PostgreSQL database:

```text
ai_powered_lms
```

Run migrations:

```bash
flask --app run.py db upgrade
flask --app run.py db current
flask --app run.py db history
```

Start backend:

```bash
flask --app run.py run
```

Backend:

```text
http://localhost:5000
```

API base:

```text
http://localhost:5000/api/v1
```

Health:

```http
GET /api/v1/health
```

## Create Admin

Public registration deliberately accepts only Student and Instructor accounts.

```bash
flask --app run.py create-admin
```

## Environment

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ai_powered_lms
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ACCESS_TOKEN_EXPIRES_HOURS=2
FRONTEND_ORIGIN=http://localhost:5173
```

Never commit the real `.env`.

## API Groups

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Courses

```text
GET    /api/v1/courses
GET    /api/v1/courses/{id}
POST   /api/v1/courses
PUT    /api/v1/courses/{id}
DELETE /api/v1/courses/{id}
PATCH  /api/v1/courses/{id}/publish
GET    /api/v1/instructor/courses
```

### Modules

```text
GET    /api/v1/courses/{course_id}/modules
POST   /api/v1/courses/{course_id}/modules
PUT    /api/v1/modules/{id}
DELETE /api/v1/modules/{id}
```

### Lessons

```text
GET    /api/v1/modules/{module_id}/lessons
POST   /api/v1/modules/{module_id}/lessons
GET    /api/v1/lessons/{id}
PUT    /api/v1/lessons/{id}
DELETE /api/v1/lessons/{id}
```

### Enrollment

```text
POST /api/v1/courses/{course_id}/enroll
GET  /api/v1/students/me/courses
GET  /api/v1/courses/{course_id}/students
```

### Progress

```text
POST /api/v1/lessons/{lesson_id}/complete
GET  /api/v1/courses/{course_id}/progress
GET  /api/v1/courses/{course_id}/students/{student_id}/progress
```

### Quizzes

```text
POST /api/v1/courses/{course_id}/quizzes
GET  /api/v1/courses/{course_id}/quizzes
GET  /api/v1/quizzes/{quiz_id}
POST /api/v1/quizzes/{quiz_id}/submit
GET  /api/v1/students/me/quiz-attempts
```

### Admin

```text
GET /api/v1/admin/users
GET /api/v1/admin/courses
```

## Standard Error Shape

```json
{
  "error": "COURSE_NOT_FOUND",
  "message": "Course does not exist.",
  "details": null
}
```

## Quiz Security

Student-facing quiz retrieval does not expose `is_correct`.

The client never supplies the authoritative score. Flask validates the submitted
question/option IDs and calculates the score server-side before storing `QuizAttempt` and
`StudentAnswer` rows.

## Progress

```text
completed lessons / total lessons * 100
```

Progress is derived from Student-Lesson records, not stored globally on Course.

## CORS

The backend allows the configured `FRONTEND_ORIGIN` for `/api/*` requests and permits the
`Authorization` header. Do not solve CORS by disabling browser security.

## Tests

```bash
pytest
```

The default test database is SQLite in-memory. For PostgreSQL-specific verification:

```dotenv
TEST_DATABASE_URL=postgresql+psycopg://...
```

## AI Boundary

No AI implementation is included here. Phase 5 explicitly completes the core integrated LMS
before the AI/Agentic phase begins.
