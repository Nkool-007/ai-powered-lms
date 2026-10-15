# AI-Powered Learning Management System

## EDUZZA Capstone Project

The **AI-Powered Learning Management System (LMS)** is a production-style Capstone Project combining traditional learning-management functionality with meaningful AI-assisted learning.

The project is designed around three primary roles:

- Student
- Instructor
- Admin

---

## Project Objective

The final application will demonstrate:

- React Frontend
- Python Flask REST API
- PostgreSQL
- SQLAlchemy
- Database relationships
- Database migrations
- JWT authentication
- Role-based authorization
- AI/Agentic functionality
- Docker
- Cloud deployment
- Automated testing
- Professional documentation

---

## Product Vision

The system is intended to support the following Student journey:

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
Ask AI Tutor
```

Instructor journey:

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

---

## Phase 1 — Product Discovery, Requirements & Scope

Phase 1 defined:

- Product requirements
- Personas
- User problems
- User stories
- Feature priorities
- MVP boundaries
- AI vision
- Out-of-scope functionality

Phase 1 documents:

```text
docs/
├── PRD.md
├── user-stories.md
├── features.md
└── scope.md
```

---

## Phase 2 — System Architecture, Database Design & API Design

Phase 2 converts the approved product requirements into a technical blueprint.

It defines:

- High-level system architecture
- Component responsibilities
- Frontend/backend communication
- Authentication architecture
- Role-based authorization
- Relational database design
- Primary and foreign keys
- Database relationships
- Data constraints
- Database migration strategy
- Entity Relationship Diagram
- REST API contract
- API authorization rules
- Standard error responses
- AI integration boundary
- AI Tutor access control
- Failure behaviour

---

## Phase 2 Repository Documents

```text
docs/
├── architecture.md
├── database-design.md
├── ER-diagram.png
└── API-design.md
```

---

## Current Repository Structure

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
└── README.md
```

---

## Reference Architecture

```text
                         USERS
                           │
                           ▼
                    React Frontend
                           │
                      HTTPS / JSON
                           │
                           ▼
                    Flask REST API
                     /           \
                    /             \
                   ▼               ▼
             PostgreSQL        AI Service
                                  │
                                  ▼
                             Vector Store
                                  │
                                  ▼
                                 LLM
```

The Flask backend is the authoritative application layer.

React does not directly access PostgreSQL.

AI functionality does not bypass normal authorization rules.

---

## Core Database Model

The core entities are:

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
AIConversation
AIMessage
```

Important relationships include:

```text
Instructor → Courses
Course → Modules
Module → Lessons
Student → Enrollment → Course
Student → LessonProgress → Lesson
Course → Quiz → Question → AnswerOption
Student → QuizAttempt → StudentAnswer
Student + Course → AIConversation → AIMessage
```

---

## Authentication & Authorization

The project uses JWT-based authentication.

Roles:

```text
STUDENT
INSTRUCTOR
ADMIN
```

Authentication answers:

> **Who is the user?**

Authorization answers:

> **What is the user allowed to do?**

Backend authorization is mandatory even when the frontend hides inaccessible functionality.

---

## AI Architecture

The flagship AI functionality is a:

### Course-Aware AI Tutor

Conceptual flow:

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

The AI system must not provide restricted Course content to an unauthorized Student.

---

## Phase 2 Status

**Phase 2 — Complete**

The project now has a documented technical blueprint covering:

```text
Product Requirements
        ↓
Architecture
        ↓
Database Model
        ↓
Entity Relationships
        ↓
REST API Contract
        ↓
Authentication / Authorization
        ↓
AI Integration Boundary
```

The project is ready to proceed to:

## Phase 3 — Backend Development

The next phase will convert the approved technical design into a working Flask REST API and relational database implementation.
