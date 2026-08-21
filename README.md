# AI-Powered Learning Management System

## EDUZZA Capstone Project

This repository contains the planning and documentation for the **AI-Powered Learning Management System (LMS)** Capstone Project.

The project is intended to become a production-style learning platform that combines traditional LMS functionality with meaningful AI-assisted learning.

## Project Objective

The final application is expected to include:

- React frontend
- Python REST API
- Relational database
- Database relationships and migrations
- JWT-based authentication
- Role-based authorization
- At least one meaningful AI/agentic feature
- Dockerisation
- Cloud deployment
- Automated tests
- Professional project documentation

## Product Vision

The LMS supports three primary user roles:

- **Student**
- **Instructor**
- **Admin**

Students should be able to discover courses, enroll, learn through structured modules and lessons, attempt quizzes, track progress, and ask an AI Learning Assistant for help.

Instructors should be able to create and organize courses, publish learning content, create assessments, and monitor student progress.

Administrators should have basic platform-level visibility and governance capabilities.

The AI layer is intended to enhance learning rather than act as a disconnected chatbot.

## Phase 1 — Product Discovery, Requirements & Scope Definition

Phase 1 focuses on understanding **what needs to be built and why** before moving into architecture and implementation.

No production coding is required for Phase 1.

The Phase 1 deliverables are stored in the `docs/` directory:

```text
ai-powered-lms/
│
├── docs/
│   ├── PRD.md
│   ├── user-stories.md
│   ├── features.md
│   └── scope.md
│
└── README.md
```

## Phase 1 Documents

### `docs/PRD.md`

Contains the Product Requirements Document, including:

- Product overview
- Problem statement
- Product vision
- Target users
- User problems
- Product goals
- Core user journeys
- AI vision
- Success criteria

### `docs/user-stories.md`

Contains prioritized user stories for:

- Students
- Instructors
- Admins
- AI-related functionality
- Overall system behavior
- Explicitly out-of-scope functionality

Priority categories used:

- **MUST HAVE**
- **SHOULD HAVE**
- **COULD HAVE**
- **OUT OF SCOPE**

### `docs/features.md`

Contains the feature catalogue organized by system:

1. Authentication & Authorization
2. Course Management
3. Module & Lesson Management
4. Course Enrollment
5. Learning & Content Delivery
6. Quiz & Assessment
7. Progress Tracking
8. AI Features
9. Admin Features
10. Integrations
11. DevOps / Production Requirements

### `docs/scope.md`

Defines the project boundaries:

- Mandatory MVP
- Optional / Should Have features
- Stretch goals
- Explicitly out-of-scope functionality
- MVP user journeys
- AI scope boundary
- Scope control rules

## Mandatory MVP Summary

The core product should support the following end-to-end student journey:

**Register → Login → Browse → View Course → Enroll → Learn → Complete Lessons → Attempt Quiz → View Score → Track Progress → Ask AI Tutor**

The core instructor journey should be:

**Login → Create Course → Add Modules → Add Lessons → Create Quiz → Publish → View Students and Progress**

The core Admin journey should be:

**Login → View Users → View Courses → Perform Basic Administration**

## AI Vision

The primary AI capability is a **Course-Aware AI Learning Assistant**.

The AI should help students:

- Ask course-related questions
- Understand difficult concepts
- Receive simpler explanations

A secondary optional capability is an **AI Quiz Generator** for instructors. AI-generated questions should be reviewed by the instructor before becoming official course content.

## Scope Principle

The project follows one key rule:

> **A complete smaller product is better than an incomplete larger product.**

The project will not attempt to recreate all functionality of Udemy, Coursera, Moodle, Google Classroom, or ChatGPT.

## Current Status

**Phase 1: Product Discovery, Requirements & Scope Definition**

The current repository establishes the product definition and MVP boundaries before system architecture, database design, backend development, frontend development, AI implementation, testing, Dockerisation, and cloud deployment begin.
