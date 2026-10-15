# AI-Powered Learning Management System (LMS)

## EDUZZA Capstone Project — Implementation Through Phase 3

The **AI-Powered Learning Management System (LMS)** is a production-style EDUZZA capstone project designed to combine conventional learning-management functionality with meaningful AI-assisted learning.

**Current milestone: Phase 3 — Backend Development (Complete).** The project has completed product discovery, technical design, and a working Python Flask REST backend. The **React frontend and Course-Aware AI Tutor are planned for later phases** and are **not represented as implemented in Phase 3**.

The system is designed around three user roles:

- **Student** — browses published courses, enrolls, learns, completes lessons, tracks progress, and attempts quizzes.
- **Instructor** — creates and publishes courses, organizes modules and lessons, creates quizzes, and monitors enrolled students.
- **Admin** — has basic administrative visibility into users and courses.

---

## 1. Project Status and Roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| **Phase 1** | Product Discovery, Requirements & Scope | **Complete** |
| **Phase 2** | System Architecture, Database Design & API Design | **Complete** |
| **Phase 3** | Flask REST API & Relational Backend Implementation | **Complete** |
| **Phase 4** | React Frontend Development | **Next** |
| **Later phases** | Course-Aware AI Tutor, additional production/deployment capabilities | **Planned; not part of Phase 3** |

### Project objectives

The **overall project vision** includes:

- React frontend.
- Python Flask REST API.
- PostgreSQL database and SQLAlchemy ORM.
- Relational data modeling and database migrations.
- JWT authentication and role-based authorization.
- Course, module, lesson, enrollment, progress, and quiz workflows.
- AI/agentic learning functionality.
- Docker, cloud deployment, automated testing, and professional documentation.

**Implementation boundary:** Phase 3 provides the independently demonstrable backend and its tests. Mention of React, the AI Tutor, vector retrieval, an LLM, Docker, or cloud deployment elsewhere in this README describes the *overall vision* unless explicitly labeled as implemented.

---

## 2. Technology Stack

| Area | Technology | Phase 3 status |
| --- | --- | --- |
| Backend | **Python 3.11+ / Flask** | Implemented |
| API | **REST / JSON** | Implemented |
| Database | **PostgreSQL** | Implemented |
| ORM | **SQLAlchemy** | Implemented |
| Schema migrations | **Alembic / Flask-Migrate** | Implemented |
| Authentication | **JWT** | Implemented |
| Password security | **Werkzeug password hashing** | Implemented |
| Tests | **pytest**; SQLite in-memory by default, optional PostgreSQL test DB | Included |
| Frontend | **React** | Planned for Phase 4 |
| AI learning support | **Course-Aware AI Tutor / LLM integration** | Planned for later phase |
| AI retrieval | **Course-specific retrieval / potential vector store** | Conceptual only |
| Containerization / hosting | **Docker / cloud deployment** | Overall project objectives; not claimed as delivered in Phase 3 |

---

## 3. Product Vision and User Journeys

### Student journey — target end-to-end experience

```text
Register
   ↓
Login
   ↓
Browse Courses
   ↓
Enroll
   ↓
Learn
   ↓
Complete Lessons
   ↓
Attempt Quiz
   ↓
Track Progress
   ↓
Ask AI Tutor  (planned for a later phase)
```

The backend workflows through quiz attempts and progress tracking are covered in Phase 3. The browser-based React experience and AI Tutor are future work.

### Instructor journey — target end-to-end experience

```text
Login
   ↓
Create Course
   ↓
Create Modules
   ↓
Create Lessons
   ↓
Create Quiz
   ↓
Publish
   ↓
Monitor Students
```

Phase 3 supports these instructor operations through REST endpoints; the frontend interface is planned for Phase 4.

---

## 4. Phase 1 — Product Discovery, Requirements & Scope

**Status: Complete**

Phase 1 defined:

- Product requirements.
- User personas and user problems.
- User stories.
- Feature priorities.
- Minimum Viable Product (MVP) boundaries.
- AI vision.
- Out-of-scope functionality.

**Phase 1 documentation**

```text
docs/
├── PRD.md
├── user-stories.md
├── features.md
└── scope.md
```

---

## 5. Phase 2 — System Architecture, Database Design & API Design

**Status: Complete**

Phase 2 transformed the product requirements into a documented technical blueprint covering:

- High-level system architecture and component responsibilities.
- Frontend/backend communication.
- Authentication architecture and role-based authorization.
- Relational database design, keys, relationships, and constraints.
- Database migration strategy and entity-relationship diagram.
- REST API contracts, authorization rules, and standard error responses.
- AI integration boundaries, planned Tutor access control, and failure behavior.

**Phase 2 documentation**

```text
docs/
├── architecture.md
├── database-design.md
├── ER-diagram.png
└── API-design.md
```

### Phase 2 reference architecture — full-system vision

```text
                         USERS
                           │
                           ▼
                     React Frontend
                      (Phase 4)
                           │
                       HTTPS / JSON
                           │
                           ▼
                     Flask REST API
                      /          \
                     /            \
                    ▼              ▼
             PostgreSQL        AI Service
             (Phase 3)       (later phase)
                                    │
                                    ▼
                               Vector Store
                                (planned)
                                    │
                                    ▼
                                   LLM
                                (planned)
```

The Flask backend is the authoritative application layer. React does **not** access PostgreSQL directly. Future AI operations must also respect authentication and course-enrollment authorization.

---

## 6. Phase 3 — Backend Development

**Status: Complete**

Phase 3 converts the approved architecture into a working Flask REST API backed by SQLAlchemy and PostgreSQL.

### Implemented backend capabilities

- User registration and login.
- JWT-based authentication.
- Student, Instructor, and Admin roles.
- Role-based authorization.
- Instructor course ownership checks.
- Course creation, retrieval, updating, deletion, and publishing.
- Course modules and lessons.
- Student course enrollment and duplicate-enrollment prevention.
- Lesson completion and student-specific progress calculation.
- Quiz creation, multiple-choice questions, submission, and server-side scoring.
- Quiz attempt history.
- Basic Admin user/course visibility.
- PostgreSQL persistence and SQLAlchemy relationships.
- Alembic/Flask-Migrate database migrations.
- Standardized API errors.

**Not included yet:** React frontend and AI Tutor functionality. The Phase 3 backend is intentionally independently usable via API clients such as Postman.

### Implemented backend request flow

```text
Browser / Postman / API Client
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

---

## 7. Repository Layout

The documentation and backend entry points explicitly referenced by the Phase 1–3 READMEs are:

```text
ai-powered-lms/
│
├── docs/
│   ├── PRD.md
│   ├── user-stories.md
│   ├── features.md
│   ├── scope.md
│   ├── architecture.md
│   ├── database-design.md
│   ├── ER-diagram.png
│   └── API-design.md
│
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── run.py
│   └── POSTMAN-DEMO.md
│
└── README.md
```

*This is a reference layout showing named files from the supplied READMEs, not an exhaustive inventory of backend source, migrations, or test modules.*

---

## 8. Data Model and Relationships

### Core LMS entities

```text
User
Course
Module
Lesson
Enrollment
LessonProgress
Quiz
Question
AnswerOption
QuizAttempt
StudentAnswer
```

### Planned AI entities from the Phase 2 design

```text
AIConversation
AIMessage
```

These AI-related entities belong to the planned AI feature design; this README does not claim the AI Tutor workflow was implemented in Phase 3.

### Key relationships

```text
Instructor → Courses
Course → Modules
Module → Lessons
Student → Enrollment → Course
Student → LessonProgress → Lesson
Course → Quiz → Question → AnswerOption
Student → QuizAttempt → StudentAnswer

Planned:
Student + Course → AIConversation → AIMessage
```

### Important database constraints

| Entity | Constraint | Purpose |
| --- | --- | --- |
| User | `UNIQUE(email)` | Prevent duplicate user accounts sharing an email |
| Enrollment | `UNIQUE(student_id, course_id)` | Prevent duplicate course enrollment |
| LessonProgress | `UNIQUE(student_id, lesson_id)` | Keep one progress record per student and lesson |
| StudentAnswer | `UNIQUE(quiz_attempt_id, question_id)` | Prevent multiple answer rows for the same question in one attempt |

### Progress calculation

```text
                   Completed Lessons
Course Progress = ------------------- × 100
                      Total Lessons
```

Progress is **specific to a student and course**; it is not stored directly on the Course.

---

## 9. Authentication, Authorization, and Security Rules

The system uses **JWT authentication** with three roles:

```text
STUDENT
INSTRUCTOR
ADMIN
```

- **Authentication:** Who is the user?
- **Authorization:** What is that user allowed to do?

For endpoints requiring authentication, send:

```http
Authorization: Bearer <JWT>
```

The backend performs authorization even if a future frontend hides unavailable actions.

### Student permissions

Students can:

- Browse published courses.
- Enroll in courses.
- Access lessons in courses in which they are enrolled.
- Mark lessons complete.
- Track their own progress.
- Attempt quizzes.
- View their quiz attempt history.

Students cannot create or edit instructor content or access another student's private information.

### Instructor permissions

Instructors can:

- Create, edit, and publish **their own** courses.
- Create modules, lessons, and quizzes for their courses.
- View enrolled students and student progress within their courses.

An Instructor **cannot** modify another Instructor's course.

### Admin account creation

Public registration must **not** create Admin accounts. Phase 3 provides a dedicated administration command:

```bash
flask --app run.py create-admin
```

Follow the command's prompts to create an Admin account.

### Quiz security

- Students must not receive `is_correct` flags before submitting a quiz.
- Scoring is performed on the backend.
- The backend does not accept client-supplied scores as authoritative.

---

## 10. Getting Started — Phase 3 Backend

### Prerequisites

Install:

- Python **3.11+**.
- PostgreSQL.
- Git.

### 10.1 Clone the repository

```bash
git clone https://github.com/Nkool-007/ai-powered-lms.git
cd ai-powered-lms
```

### 10.2 Create and activate a virtual environment

```bash
cd backend
python -m venv .venv
```

On **macOS / Linux**:

```bash
source .venv/bin/activate
```

On **Windows**:

```bat
.venv\Scripts\activate
```

### 10.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 10.4 Configure environment variables

Create a `.env` file based on `backend/.env.example`.

Example configuration:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ai_powered_lms
JWT_SECRET_KEY=replace-with-a-secure-secret
JWT_ACCESS_TOKEN_EXPIRES_HOURS=2
```

**Security:** Replace the sample secret with a strong secret and never commit the real `.env` file.

### 10.5 Create and migrate the database

Create a PostgreSQL database called:

```text
ai_powered_lms
```

From the `backend` directory, apply migrations:

```bash
flask --app run.py db upgrade
```

Check the current migration:

```bash
flask --app run.py db current
```

View migration history:

```bash
flask --app run.py db history
```

### 10.6 Create an Admin account (optional)

```bash
flask --app run.py create-admin
```

### 10.7 Run the Flask server

```bash
flask --app run.py run
```

Alternatively:

```bash
python run.py
```

Default URLs:

| Endpoint | URL |
| --- | --- |
| Flask server | `http://localhost:5000` |
| API base | `http://localhost:5000/api/v1` |

### 10.8 Verify the health endpoint

```http
GET /api/v1/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 11. Phase 3 REST API Reference

**Base URL:** `http://localhost:5000/api/v1`

The following routes are listed in the Phase 3 implementation README. Protected routes require appropriate JWT authentication and role/ownership permissions.

### Health

```http
GET /api/v1/health
```

### Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Courses

```http
GET    /api/v1/courses
GET    /api/v1/courses/{id}
POST   /api/v1/courses
PUT    /api/v1/courses/{id}
DELETE /api/v1/courses/{id}
PATCH  /api/v1/courses/{id}/publish
GET    /api/v1/instructor/courses
```

### Modules

```http
GET    /api/v1/courses/{course_id}/modules
POST   /api/v1/courses/{course_id}/modules
PUT    /api/v1/modules/{id}
DELETE /api/v1/modules/{id}
```

### Lessons

```http
GET    /api/v1/modules/{module_id}/lessons
POST   /api/v1/modules/{module_id}/lessons
GET    /api/v1/lessons/{id}
PUT    /api/v1/lessons/{id}
DELETE /api/v1/lessons/{id}
```

### Enrollment

```http
POST /api/v1/courses/{id}/enroll
GET  /api/v1/students/me/courses
GET  /api/v1/courses/{id}/students
```

### Progress

```http
POST /api/v1/lessons/{id}/complete
GET  /api/v1/courses/{id}/progress
GET  /api/v1/courses/{course_id}/students/{student_id}/progress
```

### Quizzes

```http
POST /api/v1/courses/{course_id}/quizzes
GET  /api/v1/quizzes/{id}
POST /api/v1/quizzes/{id}/submit
GET  /api/v1/students/me/quiz-attempts
```

### Admin

```http
GET /api/v1/admin/users
GET /api/v1/admin/courses
```

For the full intended request/response design, consult `docs/API-design.md`. For the walkthrough of Phase 3's implemented behavior, consult `backend/POSTMAN-DEMO.md`.

---

## 12. Testing and Verification

### Automated tests

From the `backend` directory, run:

```bash
pytest
```

The Phase 3 reference tests use **SQLite in-memory by default** for fast execution. A separate PostgreSQL test database can be configured using:

```dotenv
TEST_DATABASE_URL=<test-database-connection-url>
```

A local SQLite test run is not a substitute for confirming database-specific behavior against PostgreSQL.

### Manual API demonstration

Follow:

```text
backend/POSTMAN-DEMO.md
```

**Instructor workflow:**

```text
Register → Login → Create Course → Create Module → Create Lesson
→ Create Quiz → Publish
```

**Student workflow:**

```text
Register → Login → Browse Courses → Enroll → Access Lesson
→ Complete Lesson → View Progress → Attempt Quiz → View Result
```

Phase 3 is designed to work **without React** and to be demonstrated through REST API tooling.

---

## 13. Course-Aware AI Tutor — Planned for a Later Phase

The flagship AI capability in the Phase 2 design is a **Course-Aware AI Tutor**.

**Conceptual (not yet implemented) flow:**

```text
Student Question
       ↓
Authentication
       ↓
Enrollment Check
       ↓
Course-Specific Retrieval
       ↓
Relevant Course Context
       ↓
LLM
       ↓
AI Answer
```

The planned AI system must **not** disclose restricted course content to a student who is not authorized to access that course. Normal authentication, authorization, and enrollment checks remain enforced through the backend.

---

## 14. Completed Milestones and Next Steps

### Phase 1 complete

The product scope, requirements, personas, user stories, priorities, and AI vision have been documented.

### Phase 2 complete

The system architecture, database relationships, API design, authorization rules, and AI integration boundary have been documented.

### Phase 3 complete

The Flask REST backend provides authentication, course management, modules, lessons, enrollment, progress tracking, quizzes, basic Admin visibility, persistence, migrations, and API testing guidance.

### Phase 4 next — React Frontend Development

Build the React interface on top of the completed REST API so that students and instructors can use these workflows through a browser rather than only through API clients.

The AI Tutor, Docker, and cloud deployment remain part of the broader project objectives; **they are not claimed as Phase 3 deliverables**.

---

## 15. Engineering Principles

1. **Backend authorization is authoritative.** Hiding an action in the UI never replaces server-side checks.
2. **Course ownership is enforced.** Instructors can modify only their own courses.
3. **Data integrity is enforced at the database level.** Unique constraints prevent duplicate enrollments, lesson-progress records, and answers.
4. **Quiz scores are calculated by the server.** The system does not trust a client-submitted score.
5. **Phase 3 operates independently of React.** Backend behavior can be tested using API clients.
6. **Planned features are clearly differentiated from implemented features.** Documentation of an AI Tutor or deployment target is not proof that it is already operational.

---

**EDUZZA Capstone Project — Documentation and backend implementation completed through Phase 3.**
