# AI-Powered Learning Management System

## EDUZZA Capstone Project - Phase 3 Reference Solution

The AI-Powered Learning Management System is a production-style Capstone Project combining traditional LMS functionality with AI-assisted learning.

The system supports three primary roles:

- Student
- Instructor
- Admin

## Technology Stack

- Frontend: React
- Backend: Python Flask
- API: REST
- ORM: SQLAlchemy
- Database: PostgreSQL
- Database Migrations: Alembic / Flask-Migrate
- Authentication: JWT
- Password Security: Werkzeug Password Hashing

## Current Project Status

- Phase 1 - Complete: Product Discovery, Requirements and Scope
- Phase 2 - Complete: System Architecture, Database Design and API Design
- Phase 3 - Complete: Backend Development

## Phase 3 Backend Capabilities

The backend currently supports:

- User registration
- User login
- JWT authentication
- Student role
- Instructor role
- Admin role
- Role-based authorization
- Instructor course ownership
- Course CRUD
- Course publishing
- Modules
- Lessons
- Student enrollment
- Duplicate enrollment prevention
- Lesson completion
- Progress calculation
- Quiz creation
- Multiple-choice questions
- Quiz submission
- Server-side scoring
- Quiz attempt history
- Basic Admin visibility
- PostgreSQL persistence
- SQLAlchemy relationships
- Database migrations
- Standardized API errors

AI functionality is intentionally implemented in a later project phase.

## Backend Architecture

```text
Browser / Postman
        |
        v
Flask REST API
        |
        v
Authentication + Authorization
        |
        v
Business Logic
        |
        v
SQLAlchemy
        |
        v
PostgreSQL
```

## Prerequisites

Install:

- Python 3.11+
- PostgreSQL
- Git

## Clone Repository

```bash
git clone https://github.com/Nkool-007/ai-powered-lms.git
cd ai-powered-lms
```

## Backend Setup

```bash
cd backend
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create `.env` from `.env.example`.

Example:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ai_powered_lms
JWT_SECRET_KEY=replace-with-a-secure-secret
JWT_ACCESS_TOKEN_EXPIRES_HOURS=2
```

Never commit the real `.env` file.

## Database Setup

Create a PostgreSQL database named:

```text
ai_powered_lms
```

Run migrations:

```bash
flask --app run.py db upgrade
```

Check migration version:

```bash
flask --app run.py db current
```

View migration history:

```bash
flask --app run.py db history
```

## Create Admin

Public registration deliberately does not permit creation of Admin accounts.

```bash
flask --app run.py create-admin
```

Follow the prompts.

## Start Backend

```bash
flask --app run.py run
```

or:

```bash
python run.py
```

Default backend URL:

```text
http://localhost:5000
```

API Base URL:

```text
http://localhost:5000/api/v1
```

## Health Check

```http
GET /api/v1/health
```

Response:

```json
{
  "status": "ok"
}
```

## Authentication APIs

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

## Course APIs

```text
GET    /api/v1/courses
GET    /api/v1/courses/{id}
POST   /api/v1/courses
PUT    /api/v1/courses/{id}
DELETE /api/v1/courses/{id}
PATCH  /api/v1/courses/{id}/publish
GET    /api/v1/instructor/courses
```

## Module APIs

```text
GET    /api/v1/courses/{course_id}/modules
POST   /api/v1/courses/{course_id}/modules
PUT    /api/v1/modules/{id}
DELETE /api/v1/modules/{id}
```

## Lesson APIs

```text
GET    /api/v1/modules/{module_id}/lessons
POST   /api/v1/modules/{module_id}/lessons
GET    /api/v1/lessons/{id}
PUT    /api/v1/lessons/{id}
DELETE /api/v1/lessons/{id}
```

## Enrollment APIs

```text
POST /api/v1/courses/{id}/enroll
GET  /api/v1/students/me/courses
GET  /api/v1/courses/{id}/students
```

## Progress APIs

```text
POST /api/v1/lessons/{id}/complete
GET  /api/v1/courses/{id}/progress
GET  /api/v1/courses/{course_id}/students/{student_id}/progress
```

## Quiz APIs

```text
POST /api/v1/courses/{course_id}/quizzes
GET  /api/v1/quizzes/{id}
POST /api/v1/quizzes/{id}/submit
GET  /api/v1/students/me/quiz-attempts
```

## Admin APIs

```text
GET /api/v1/admin/users
GET /api/v1/admin/courses
```

## JWT Authentication

Protected requests must contain:

```http
Authorization: Bearer <JWT>
```

Authentication determines:

> Who is the user?

Authorization determines:

> What is the user allowed to do?

The backend remains authoritative for security.

## Student Permissions

Students can:

- Browse published courses
- Enroll
- Access enrolled course lessons
- Complete lessons
- Track progress
- Attempt quizzes
- View their quiz attempts

Students cannot:

- Create courses
- Modify instructor content
- Access another student's private information

## Instructor Permissions

Instructors can:

- Create courses
- Edit their own courses
- Create modules
- Create lessons
- Create quizzes
- Publish their courses
- View students enrolled in their courses
- View student progress

An Instructor cannot modify another Instructor's Course.

## Important Database Constraints

User email:

```text
UNIQUE(email)
```

Enrollment:

```text
UNIQUE(student_id, course_id)
```

Lesson Progress:

```text
UNIQUE(student_id, lesson_id)
```

Student Answer:

```text
UNIQUE(quiz_attempt_id, question_id)
```

## Progress Formula

```text
Completed Lessons
----------------- x 100
Total Lessons
```

Progress is student-specific. It is not stored directly on the Course.

## Quiz Security

Student Quiz responses do not contain `is_correct` before submission.

Quiz scoring is performed by the backend.

The backend does not trust a score supplied by the client.

## Manual API Testing

See:

```text
backend/POSTMAN-DEMO.md
```

The reference demonstration covers:

```text
Instructor:
Register -> Login -> Create Course -> Create Module -> Create Lesson
-> Create Quiz -> Publish

Student:
Register -> Login -> Browse -> Enroll -> Access Lesson
-> Complete Lesson -> View Progress -> Attempt Quiz -> View Result
```

## Run Tests

From the `backend` directory:

```bash
pytest
```

The included tests use SQLite in-memory by default for fast reference testing. A separate PostgreSQL testing database may be configured through:

```text
TEST_DATABASE_URL
```

## Phase 3 Engineering Principle

Phase 3 must work without React.

The backend should be independently demonstrable using Postman or Swagger/OpenAPI.

React will be introduced after the core backend is stable.

## Next Phase

### Phase 4 - React Frontend Development

The next phase will build the user interface on top of the completed REST backend.
