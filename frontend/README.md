# EDUZZA SmartLMS Frontend

## AI-Powered Learning Management System

This directory contains the Phase 4 React frontend for the EDUZZA AI-Powered LMS Capstone Project.

## Technology Stack

- Frontend: React
- Build Tool: Vite
- Routing: React Router
- HTTP Client: Axios
- Shared Authentication State: React Context API
- Styling: Bootstrap + custom CSS
- Backend: Python Flask REST API

## Current Project Status

- Phase 1 — Complete — Product Discovery, Requirements and Scope
- Phase 2 — Complete — Architecture, Database Design and API Design
- Phase 3 — Complete — Flask REST Backend
- Phase 4 — Complete — React Frontend Development
- Phase 5 — Next — Full-Stack Integration

## Phase 4 Features

### Public Experience
- Landing Page
- Login
- Registration
- Course Catalog
- Course Details

### Student Experience
- Student Dashboard
- My Courses
- Lesson Viewer
- Course Progress
- Quiz Interface
- Quiz Result
- AI Tutor UI placeholder

### Instructor Experience
- Instructor Dashboard
- Create Course
- Course Editor
- Module Manager
- Lesson Manager
- Quiz Manager
- Student Progress View
- AI Quiz Generator UI placeholder

### Application Architecture
- React Router
- Authentication Context
- Protected Routes
- Role-Aware Routes
- Reusable Components
- Services Layer
- Loading States
- Error States
- Empty States
- Responsive UI

## Prerequisites

- Node.js 18+
- npm
- A running Phase 3 Flask backend when real API calls are tested.

## Installation

```bash
cd frontend
npm install
```

## Environment Configuration

Create `.env` from `.env.example`.

```text
VITE_API_BASE_URL=http://localhost:5000/api/v1
```

Do not hard-code API URLs across components.

## Start Development Server

```bash
npm run dev
```

Typical Vite URL: `http://localhost:5173`

## Production Build

```bash
npm run build
```

Output: `dist/`

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

These routes require the `STUDENT` role.

## Instructor Routes

```text
/instructor/dashboard
/instructor/courses/new
/instructor/courses/:courseId/edit
/instructor/courses/:courseId/quiz
/instructor/courses/:courseId/students
/instructor/ai-quiz
```

These routes require the `INSTRUCTOR` role.

## Authentication Flow

```text
Login Form
   ↓
POST /auth/login
   ↓
JWT + User Returned
   ↓
JWT Stored
   ↓
AuthContext Updated
   ↓
Role-Aware Redirect
```

The access token is stored under `smartlms_access_token`.

On browser refresh:

```text
Read Token
   ↓
GET /auth/me
   ↓
Restore User
```

If the token is invalid, the frontend clears authentication state.

## Security Principle

React routing is not authorization. React protects the user experience; Flask remains the authoritative authorization layer.

## Services Layer

```text
services/
├── api.js
├── authService.js
├── courseService.js
├── enrollmentService.js
└── quizService.js
```

Pages call service functions instead of scattering independent Axios requests through components.

## APIs Used

### Authentication
```text
POST /auth/register
POST /auth/login
GET /auth/me
```

### Courses
```text
GET /courses
GET /courses/{id}
POST /courses
PUT /courses/{id}
DELETE /courses/{id}
PATCH /courses/{id}/publish
GET /instructor/courses
```

### Modules
```text
GET /courses/{course_id}/modules
POST /courses/{course_id}/modules
PUT /modules/{id}
DELETE /modules/{id}
```

### Lessons
```text
GET /modules/{module_id}/lessons
POST /modules/{module_id}/lessons
GET /lessons/{id}
PUT /lessons/{id}
DELETE /lessons/{id}
```

### Enrollment
```text
POST /courses/{course_id}/enroll
GET /students/me/courses
GET /courses/{course_id}/students
```

### Progress
```text
POST /lessons/{lesson_id}/complete
GET /courses/{course_id}/progress
GET /courses/{course_id}/students/{student_id}/progress
```

### Quiz
```text
POST /courses/{course_id}/quizzes
GET /quizzes/{quiz_id}
POST /quizzes/{quiz_id}/submit
GET /students/me/quiz-attempts
```

## Loading, Empty and Error States

Important network-driven pages handle Loading, Success, Empty, and Error states.

## Responsive Design

The application is designed for desktop, tablet, and mobile using Bootstrap's responsive grid plus custom CSS.

## AI Screens

Phase 4 contains UI shells for the AI Tutor and AI Quiz Generator. Actual LLM, RAG, embeddings, retrieval, AI Quiz generation, and Agentic AI functionality are intentionally deferred to the later AI phase.

## Known Integration Contract Gap

The current backend provides `GET /quizzes/{quiz_id}` but does not currently provide `GET /courses/{course_id}/quizzes`. Course-level quiz discovery should therefore be reviewed during Phase 5 integration.

## Phase 4 Engineering Principle

Phase 4 focuses on sound React frontend architecture: routing, component design, authentication state, protected routes, role-aware navigation, Student UX, Instructor UX, forms, loading states, empty states, error states, responsive design, and service abstraction.
