# EDUZZA SmartLMS Frontend

## Phase 4 + Phase 5 Integrated Reference Implementation

This directory contains the React frontend for the EDUZZA AI-Powered LMS Capstone Project.

It preserves the Phase 4 frontend architecture and applies the Phase 5 full-stack integration
requirements so that the UI communicates with the real Flask REST API.

## Technology Stack

- React 18
- Vite
- React Router
- Axios
- React Context API
- Bootstrap 5
- Custom CSS
- Flask REST API backend
- PostgreSQL behind Flask

## Current Project Status

- Phase 1 — Complete
- Phase 2 — Complete
- Phase 3 — Complete
- Phase 4 — Complete
- Phase 5 — Full-Stack Integration — Complete
- Phase 6 — AI Layer — Next

## Architecture

```text
User
  ↓
React
  ↓
Pages / Components
  ↓
Services
  ↓
Central Axios Client
  ↓
HTTP / JSON
  ↓
Flask REST API
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

React never connects directly to PostgreSQL.

React is responsible for presentation, interactions, client-side form validation, and UX state.

Flask remains authoritative for authentication, authorization, ownership, enrollment, scoring,
business rules, validation and persistent data.

## Project Structure

```text
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── course/
│   │   ├── lesson/
│   │   ├── progress/
│   │   └── quiz/
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── layouts/
│   ├── pages/
│   │   ├── public/
│   │   ├── student/
│   │   └── instructor/
│   ├── routes/
│   │   └── ProtectedRoute.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── courseService.js
│   │   ├── enrollmentService.js
│   │   └── quizService.js
│   ├── styles/
│   │   └── app.css
│   ├── utils/
│   │   ├── authStorage.js
│   │   ├── date.js
│   │   └── errors.js
│   ├── App.jsx
│   └── main.jsx
├── .env.example
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## Prerequisites

- Node.js 18+
- npm
- Running Phase 5 Flask backend at `http://localhost:5000`

## Installation

```bash
cd frontend
npm install
```

Create `.env` from `.env.example`:

```dotenv
VITE_API_BASE_URL=http://localhost:5000/api/v1
```

Start development server:

```bash
npm run dev
```

Typical frontend URL:

```text
http://localhost:5173
```

Build:

```bash
npm run build
```

## Authentication Integration

Login flow:

```text
Login Form
  ↓
authService.login()
  ↓
POST /auth/login
  ↓
JWT + User
  ↓
authStorage
  ↓
AuthContext
  ↓
Role-Aware Redirect
```

Stored token key:

```text
smartlms_access_token
```

On browser refresh:

```text
Read JWT
  ↓
GET /auth/me
  ↓
Restore User
```

## Centralized Axios Client

`src/services/api.js`:

- reads `VITE_API_BASE_URL`
- adds `Content-Type: application/json`
- attaches `Authorization: Bearer <JWT>` automatically
- uses a 10-second timeout
- distinguishes failed login from expired authenticated sessions
- clears stale JWT state on authenticated `401`
- dispatches `smartlms:auth-expired`

## 401 vs 403

`401` means the client is not correctly authenticated.

Examples:

- missing token
- invalid token
- expired token

When a stored token receives a 401, the session is cleared.

`403` means the user is authenticated but not authorized.

Examples:

- Student tries to create Course
- Instructor tries to edit another Instructor's Course
- unenrolled Student opens protected Lesson

A 403 does not automatically log the user out.

## Public Routes

```text
/
/login
/register
/courses
/courses/:courseId
```

## Student Routes

```text
/student/dashboard
/student/courses
/student/progress
/student/ai
/courses/:courseId/lessons/:lessonId
/quizzes/:quizId
```

## Instructor Routes

```text
/instructor/dashboard
/instructor/courses/new
/instructor/courses/:courseId/edit
/instructor/courses/:courseId/quiz
/instructor/courses/:courseId/students
/instructor/ai-quiz
```

## Real Integrated Student Workflow

```text
Login
  ↓
Browse Published Courses
  ↓
Course Details
  ↓
Enroll
  ↓
My Courses
  ↓
Open Lesson
  ↓
Mark Complete
  ↓
View Progress
  ↓
Discover Course Quizzes
  ↓
Open Quiz
  ↓
Submit Answers
  ↓
Backend Calculates Score
  ↓
View Result / Attempt History
```

## Real Integrated Instructor Workflow

```text
Login
  ↓
Instructor Dashboard
  ↓
Create Course
  ↓
Edit Course
  ↓
Add Module
  ↓
Add Lesson
  ↓
Create Quiz
  ↓
Publish
  ↓
View Enrolled Students
  ↓
View Student Progress
```

## Phase 5 Quiz Discovery

The frontend uses:

```http
GET /api/v1/courses/{course_id}/quizzes
```

This prevents hard-coded Quiz IDs.

## Quiz Security

Student quiz retrieval is expected to return:

- question ID
- question text
- option ID
- option text

It must not reveal `is_correct`.

React submits answers only:

```json
{
  "answers": [
    {
      "question_id": 11,
      "selected_option_id": 44
    }
  ]
}
```

React does not send an authoritative score.

The displayed score comes from Flask.

## Error Handling

The shared error utility handles:

- backend error message
- network unavailable
- request timeout
- fallback application error

The application should show human-readable messages such as:

```text
Unable to connect to the server.
```

rather than raw Axios internals.

## Screen State Model

API-driven screens implement:

```text
Initial
  ↓
Loading
  ↓
Success ──→ Data
  │
  └──────→ Empty

or

Error
```

## AI Boundary

The frontend includes UI placeholders for:

- Course-Aware AI Tutor
- AI Quiz Generator

No LLM, embeddings, RAG, vector database, LangChain, LangGraph or Agentic AI functionality
is implemented in Phase 5. That belongs to the next AI phase.

## Required Backend Environment

The compatible backend should include:

```dotenv
FRONTEND_ORIGIN=http://localhost:5173
```

and expose:

```text
http://localhost:5000/api/v1
```

## Two-Terminal Development Workflow

Terminal 1:

```bash
cd backend
source .venv/bin/activate
flask --app run.py run
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```
