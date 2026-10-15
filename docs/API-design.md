# AI-Powered LMS — REST API Design

## 1. API Overview

The React frontend communicates with the Flask backend through a versioned REST API.

```text
React
  │
  │ HTTPS + JSON
  ▼
Flask REST API
  │
  │ SQLAlchemy
  ▼
PostgreSQL
```

React does not directly access PostgreSQL.

The API is responsible for:

- Authentication
- Authorization
- Validation
- LMS business rules
- Database operations
- AI integration
- Standardized errors

---

## 2. Base URL

```text
/api/v1
```

Examples:

```text
/api/v1/auth/login
/api/v1/courses
/api/v1/ai/chat
```

Versioning allows future breaking changes to be introduced under `/api/v2` without immediately breaking existing clients.

---

## 3. Content Type

Requests and responses primarily use:

```http
Content-Type: application/json
```

---

## 4. Authentication Model

Protected endpoints require:

```http
Authorization: Bearer <JWT>
```

The JWT identifies the authenticated User.

For the MVP, the token represents:

- User identity
- Role
- Expiration

---

## 5. Standard Success Structure

```json
{
  "data": {
    "id": 12,
    "title": "Python Fundamentals"
  }
}
```

Collection example:

```json
{
  "data": [
    {
      "id": 12,
      "title": "Python Fundamentals"
    }
  ]
}
```

---

## 6. Standard Error Structure

```json
{
  "error": "COURSE_NOT_FOUND",
  "message": "Course does not exist.",
  "details": null
}
```

Validation example:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Request data is invalid.",
  "details": {
    "email": "A valid email address is required."
  }
}
```

---

## 7. Important HTTP Status Codes

| Code | Meaning |
|---:|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Successful request with no response body |
| 400 | Invalid request |
| 401 | Authentication missing/invalid |
| 403 | Authenticated but not permitted |
| 404 | Resource not found |
| 409 | Conflict with existing state |
| 500 | Unexpected server error |
| 503 | Dependency/service temporarily unavailable |

---

## 8. Authentication Endpoints

### 8.1 Register

```http
POST /api/v1/auth/register
```

**Purpose:** Create a new Student or Instructor account.

Admin accounts cannot be created through public registration.

**Authentication:** Not required.

**Request:**

```json
{
  "name": "Aman Sharma",
  "email": "aman@example.com",
  "password": "StrongPassword123",
  "role": "STUDENT"
}
```

Allowed public roles:

```text
STUDENT
INSTRUCTOR
```

**Success:** `201 Created`

```json
{
  "data": {
    "id": 15,
    "name": "Aman Sharma",
    "email": "aman@example.com",
    "role": "STUDENT"
  }
}
```

**Important Errors:**

```text
400 INVALID_ROLE
400 VALIDATION_ERROR
409 EMAIL_ALREADY_REGISTERED
```

---

## 9. Login

```http
POST /api/v1/auth/login
```

**Authentication:** Not required.

**Request:**

```json
{
  "email": "aman@example.com",
  "password": "StrongPassword123"
}
```

**Success:**

```json
{
  "data": {
    "access_token": "<JWT>",
    "user": {
      "id": 15,
      "name": "Aman Sharma",
      "email": "aman@example.com",
      "role": "STUDENT"
    }
  }
}
```

**Errors:**

```text
401 INVALID_CREDENTIALS
403 ACCOUNT_DISABLED
```

---

## 10. Current User

```http
GET /api/v1/auth/me
```

**Authentication:** Required.

**Allowed Roles:** All authenticated users.

**Success:**

```json
{
  "data": {
    "id": 15,
    "name": "Aman Sharma",
    "email": "aman@example.com",
    "role": "STUDENT"
  }
}
```

---

## 11. Logout

For stateless MVP JWT authentication, the frontend can discard the token.

An optional endpoint may be exposed as:

```http
POST /api/v1/auth/logout
```

Server-side token revocation is not mandatory in the MVP.

---

## 12. Course Endpoints

### 12.1 List Published Courses

```http
GET /api/v1/courses
```

**Authentication:** Not required.

**Purpose:** Return published Courses available for discovery.

**Success:**

```json
{
  "data": [
    {
      "id": 10,
      "title": "Python Fundamentals",
      "description": "Learn Python from first principles.",
      "instructor": {
        "id": 8,
        "name": "Instructor Name"
      }
    }
  ]
}
```

Draft Courses are excluded.

---

## 13. Get Course Details

```http
GET /api/v1/courses/{course_id}
```

Published Course:

```text
Publicly readable
```

Draft Course:

```text
Readable only by owning Instructor
```

**Possible Errors:**

```text
404 COURSE_NOT_FOUND
403 COURSE_ACCESS_DENIED
```

---

## 14. Create Course

```http
POST /api/v1/courses
```

**Authentication:** Required.

**Allowed Role:** `INSTRUCTOR`

**Request:**

```json
{
  "title": "Python Fundamentals",
  "description": "Complete introductory Python course."
}
```

**Success:** `201 Created`

```json
{
  "data": {
    "id": 17,
    "title": "Python Fundamentals",
    "description": "Complete introductory Python course.",
    "status": "DRAFT",
    "instructor_id": 8
  }
}
```

**Errors:**

```text
400 VALIDATION_ERROR
401 AUTHENTICATION_REQUIRED
403 INSUFFICIENT_PERMISSION
```

---

## 15. Update Course

```http
PUT /api/v1/courses/{course_id}
```

**Allowed:** Owning Instructor only.

**Request:**

```json
{
  "title": "Advanced Python Fundamentals",
  "description": "Updated course description."
}
```

**Errors:**

```text
403 NOT_COURSE_OWNER
404 COURSE_NOT_FOUND
```

---

## 16. Delete Course

```http
DELETE /api/v1/courses/{course_id}
```

Reference rule:

- Owning Instructor
- Course must be safe to delete
- Published Course with learner history should not be destructively removed

Possible response:

```text
204 No Content
```

Possible conflict:

```text
409 COURSE_HAS_LEARNER_DATA
```

---

## 17. Publish Course

```http
PATCH /api/v1/courses/{course_id}/publish
```

**Allowed:** Owning Instructor.

**Success:**

```json
{
  "data": {
    "id": 17,
    "status": "PUBLISHED",
    "published_at": "2026-09-03T10:00:00Z"
  }
}
```

---

## 18. Instructor's Courses

```http
GET /api/v1/instructor/courses
```

**Authentication:** Required.

**Role:** `INSTRUCTOR`

Returns both DRAFT and PUBLISHED Courses owned by the Instructor.

---

## 19. Module Endpoints

### List Modules

```http
GET /api/v1/courses/{course_id}/modules
```

Published Course outline may be publicly visible.

Full restricted learning content remains controlled at Lesson level.

### Create Module

```http
POST /api/v1/courses/{course_id}/modules
```

**Role:** Owning Instructor.

**Request:**

```json
{
  "title": "Python Basics",
  "description": "Foundational Python concepts.",
  "position": 1
}
```

**Success:** `201 Created`

### Update Module

```http
PUT /api/v1/modules/{module_id}
```

Owning Instructor only.

### Delete Module

```http
DELETE /api/v1/modules/{module_id}
```

Owning Instructor only.

Deletion may be rejected if doing so would invalidate Student learning history.

---

## 20. Lesson Endpoints

### List Lessons

```http
GET /api/v1/modules/{module_id}/lessons
```

This may return lesson metadata.

Access to full lesson content follows Course access rules.

### Create Lesson

```http
POST /api/v1/modules/{module_id}/lessons
```

**Role:** Owning Instructor.

**Request:**

```json
{
  "title": "Python Variables",
  "content": "Lesson content...",
  "position": 1
}
```

### Get Lesson

```http
GET /api/v1/lessons/{lesson_id}
```

Allowed:

- Student enrolled in the Course
- Owning Instructor
- Admin where administrative access is required

Unenrolled Student:

```text
403 COURSE_ENROLLMENT_REQUIRED
```

### Update Lesson

```http
PUT /api/v1/lessons/{lesson_id}
```

Owning Instructor.

### Delete Lesson

```http
DELETE /api/v1/lessons/{lesson_id}
```

Owning Instructor, subject to learner-data restrictions.

---

## 21. Enrollment Endpoints

### Enroll in Course

```http
POST /api/v1/courses/{course_id}/enroll
```

**Authentication:** Required.

**Role:** `STUDENT`

Requirements:

- Course exists
- Course is published
- Student is not already enrolled

**Success:** `201 Created`

```json
{
  "data": {
    "course_id": 15,
    "status": "ACTIVE",
    "message": "Enrollment successful."
  }
}
```

**Errors:**

```text
404 COURSE_NOT_FOUND
409 ALREADY_ENROLLED
403 COURSE_NOT_AVAILABLE
```

---

## 22. Student's Enrolled Courses

```http
GET /api/v1/students/me/courses
```

**Role:** STUDENT.

**Success:**

```json
{
  "data": [
    {
      "course_id": 15,
      "title": "Python Fundamentals",
      "progress_percentage": 60
    }
  ]
}
```

---

## 23. View Enrolled Students

```http
GET /api/v1/courses/{course_id}/students
```

Allowed:

- Owning Instructor
- Admin

---

## 24. Progress Endpoints

### Complete Lesson

```http
POST /api/v1/lessons/{lesson_id}/complete
```

**Role:** STUDENT.

**Requirement:** Student must be enrolled in the corresponding Course.

The operation is designed to be **idempotent**.

Submitting the same completion twice should not create duplicate LessonProgress rows.

**Success:**

```json
{
  "data": {
    "lesson_id": 22,
    "completed": true,
    "completed_at": "2026-09-03T10:30:00Z"
  }
}
```

---

## 25. Get Own Course Progress

```http
GET /api/v1/courses/{course_id}/progress
```

**Role:** STUDENT.

**Response:**

```json
{
  "data": {
    "course_id": 8,
    "completed_lessons": 12,
    "total_lessons": 20,
    "progress_percentage": 60
  }
}
```

---

## 26. Instructor Views Student Progress

```http
GET /api/v1/courses/{course_id}/students/{student_id}/progress
```

**Allowed:** Owning Instructor.

**Response:**

```json
{
  "data": {
    "student_id": 25,
    "course_id": 8,
    "completed_lessons": 12,
    "total_lessons": 20,
    "progress_percentage": 60
  }
}
```

---

## 27. Quiz Endpoints

### Create Quiz

```http
POST /api/v1/courses/{course_id}/quizzes
```

**Role:** Owning Instructor.

**Request:**

```json
{
  "title": "Python Basics Quiz",
  "description": "Assessment for Python fundamentals."
}
```

---

## 28. Get Quiz

```http
GET /api/v1/quizzes/{quiz_id}
```

Student must be enrolled.

Student response must **not expose** `is_correct` or `correct_answer` before submission.

Instructor response may include correct-answer information.

---

## 29. Example Student Quiz Response

```json
{
  "data": {
    "id": 4,
    "title": "Python Basics Quiz",
    "questions": [
      {
        "id": 51,
        "question": "Which keyword defines a function?",
        "options": [
          {
            "id": 201,
            "text": "func"
          },
          {
            "id": 202,
            "text": "def"
          }
        ]
      }
    ]
  }
}
```

Notice that this response does not contain:

```text
"is_correct": true
```

---

## 30. Submit Quiz

```http
POST /api/v1/quizzes/{quiz_id}/submit
```

**Role:** STUDENT.

**Requirement:** Student must be enrolled.

**Request:**

```json
{
  "answers": [
    {
      "question_id": 51,
      "selected_option_id": 202
    },
    {
      "question_id": 52,
      "selected_option_id": 205
    }
  ]
}
```

Backend performs:

```text
Validate Quiz
    ↓
Validate Enrollment
    ↓
Validate Questions
    ↓
Validate Options
    ↓
Calculate Correct Answers
    ↓
Calculate Score
    ↓
Create QuizAttempt
    ↓
Create StudentAnswers
```

**Success:** `201 Created`

```json
{
  "data": {
    "attempt_id": 95,
    "score": 80,
    "total_questions": 5,
    "correct_answers": 4
  }
}
```

---

## 31. Student Quiz Attempts

```http
GET /api/v1/students/me/quiz-attempts
```

Optional filter:

```http
GET /api/v1/students/me/quiz-attempts?course_id=12
```

---

## 32. Admin Endpoints

### View Users

```http
GET /api/v1/admin/users
```

**Role:** ADMIN.

### View Courses

```http
GET /api/v1/admin/courses
```

**Role:** ADMIN.

Returns both DRAFT and PUBLISHED where administratively appropriate.

---

## 33. Optional Admin Endpoints

These are SHOULD HAVE, not mandatory MVP requirements.

```http
PATCH /api/v1/admin/users/{user_id}/status
```

Example:

```json
{
  "is_active": false
}
```

And:

```http
PATCH /api/v1/admin/courses/{course_id}/status
```

for moderation.

---

## 34. AI Tutor Endpoint

```http
POST /api/v1/ai/chat
```

**Role:** STUDENT.

**Authentication:** Required.

**Authorization:** Student must be enrolled in the requested Course.

**Request:**

```json
{
  "course_id": 12,
  "conversation_id": 35,
  "message": "Explain Python decorators in simple words."
}
```

For a new conversation, `conversation_id` may be omitted or null.

---

## 35. AI Chat Backend Flow

```text
Receive Request
    ↓
Validate JWT
    ↓
Verify STUDENT Role
    ↓
Validate Course
    ↓
Verify Enrollment
    ↓
Load/Create Conversation
    ↓
Retrieve Course Context
    ↓
Call AI Service
    ↓
Store USER Message
    ↓
Store ASSISTANT Message
    ↓
Return Response
```

---

## 36. AI Chat Success Response

```json
{
  "data": {
    "conversation_id": 35,
    "answer": "A Python decorator is a function that changes or extends the behaviour of another function..."
  }
}
```

---

## 37. AI Chat Errors

```text
401 AUTHENTICATION_REQUIRED
403 COURSE_ENROLLMENT_REQUIRED
404 COURSE_NOT_FOUND
404 CONVERSATION_NOT_FOUND
503 AI_SERVICE_UNAVAILABLE
```

A Student must not be allowed to provide someone else's `conversation_id`.

---

## 38. Optional AI Quiz Generator

```http
POST /api/v1/ai/generate-quiz
```

**Role:** INSTRUCTOR.

**Requirement:** Instructor must own the Lesson's Course.

**Request:**

```json
{
  "lesson_id": 42,
  "difficulty": "medium",
  "number_of_questions": 5
}
```

**Response:**

```json
{
  "data": {
    "questions": [
      {
        "question": "What is the purpose of a Python function?",
        "options": [
          "Store files",
          "Group reusable instructions",
          "Create a database",
          "Start a server"
        ],
        "correct_option_index": 1,
        "explanation": "Functions group reusable instructions."
      }
    ]
  }
}
```

The response remains a **draft**. It is not automatically stored or published.

---

## 39. Authorization Matrix

| Endpoint | Public | Student | Instructor | Admin |
|---|---:|---:|---:|---:|
| POST `/auth/register` | Yes | — | — | No |
| POST `/auth/login` | Yes | Yes | Yes | Yes |
| GET `/auth/me` | No | Yes | Yes | Yes |
| GET `/courses` | Yes | Yes | Yes | Yes |
| GET `/courses/{id}` | Published | Yes | Yes | Yes |
| POST `/courses` | No | No | Yes | No |
| PUT `/courses/{id}` | No | No | Owner | No |
| PATCH `/courses/{id}/publish` | No | No | Owner | No |
| DELETE `/courses/{id}` | No | No | Owner | No |
| POST `/courses/{id}/modules` | No | No | Owner | No |
| POST `/modules/{id}/lessons` | No | No | Owner | No |
| GET `/lessons/{id}` | No | Enrolled | Owner | Yes |
| POST `/courses/{id}/enroll` | No | Yes | No | No |
| GET `/students/me/courses` | No | Yes | No | No |
| GET `/courses/{id}/students` | No | No | Owner | Yes |
| POST `/lessons/{id}/complete` | No | Enrolled | No | No |
| GET `/courses/{id}/progress` | No | Enrolled | No | No |
| POST `/courses/{id}/quizzes` | No | No | Owner | No |
| GET `/quizzes/{id}` | No | Enrolled | Owner | Yes |
| POST `/quizzes/{id}/submit` | No | Enrolled | No | No |
| GET `/students/me/quiz-attempts` | No | Yes | No | No |
| POST `/ai/chat` | No | Enrolled | No | No |
| POST `/ai/generate-quiz` | No | No | Owner | No |
| GET `/admin/users` | No | No | No | Yes |
| GET `/admin/courses` | No | No | No | Yes |

---

## 40. Core Error Codes

Suggested standardized codes:

```text
VALIDATION_ERROR
AUTHENTICATION_REQUIRED
INVALID_CREDENTIALS
TOKEN_EXPIRED
INSUFFICIENT_PERMISSION
NOT_COURSE_OWNER
COURSE_NOT_FOUND
MODULE_NOT_FOUND
LESSON_NOT_FOUND
QUIZ_NOT_FOUND
COURSE_ENROLLMENT_REQUIRED
ALREADY_ENROLLED
EMAIL_ALREADY_REGISTERED
ACCOUNT_DISABLED
INVALID_QUIZ_SUBMISSION
AI_SERVICE_UNAVAILABLE
DATABASE_UNAVAILABLE
INTERNAL_SERVER_ERROR
```

---

## 41. Requirements Traceability Matrix

| Phase 1 Requirement | Database Entity | Primary API |
|---|---|---|
| User can register | User | POST `/auth/register` |
| User can login | User | POST `/auth/login` |
| Instructor creates course | Course | POST `/courses` |
| Instructor creates modules | Module | POST `/courses/{id}/modules` |
| Instructor creates lessons | Lesson | POST `/modules/{id}/lessons` |
| Student browses courses | Course | GET `/courses` |
| Student enrolls | Enrollment | POST `/courses/{id}/enroll` |
| Student views own courses | Enrollment + Course | GET `/students/me/courses` |
| Student accesses lesson | Lesson + Enrollment | GET `/lessons/{id}` |
| Student completes lesson | LessonProgress | POST `/lessons/{id}/complete` |
| Student views progress | LessonProgress | GET `/courses/{id}/progress` |
| Instructor creates quiz | Quiz, Question, AnswerOption | POST `/courses/{id}/quizzes` |
| Student attempts quiz | QuizAttempt, StudentAnswer | POST `/quizzes/{id}/submit` |
| Student views results | QuizAttempt | GET `/students/me/quiz-attempts` |
| Student asks AI | AIConversation, AIMessage | POST `/ai/chat` |
| Instructor generates AI quiz | Lesson + AI Service | POST `/ai/generate-quiz` |
| Admin views users | User | GET `/admin/users` |
| Admin views courses | Course | GET `/admin/courses` |

---

## 42. API Design Principles

The API follows these rules:

1. Resource-oriented URLs.
2. Consistent `/api/v1` prefix.
3. Appropriate HTTP methods.
4. JSON requests and responses.
5. Backend authorization.
6. Consistent error format.
7. Correct use of HTTP status codes.
8. No direct frontend-to-database access.
9. Correct answers hidden before Quiz submission.
10. AI endpoints obey Course access rules.
