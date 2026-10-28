# AI-Powered LMS — REST API Design
## 1. API Overview
The React frontend communicates with the Flask backend through a versioned REST API.

Architecture:

React
 │
 │ HTTPS + JSON
 ▼
Flask REST API
 │
 │ SQLAlchemy
 ▼
PostgreSQL

React does not directly access PostgreSQL.

The API is responsible for:

- Authentication.
- Authorization.
- Validation.
- LMS business rules.
- Database operations.
- AI integration.
- Standardized errors.


## 2. Base URL
/api/v1

Examples:

/api/v1/auth/login
/api/v1/courses
/api/v1/ai/chat

Versioning allows future breaking changes to be introduced under:

/api/v2

without immediately breaking existing clients.


## 3. Content Type
Requests and responses primarily use:

Content-Type: application/json


## 4. Authentication Model
Protected endpoints require:

Authorization: Bearer <JWT>

The JWT identifies the authenticated User.

For the MVP, the token represents:

- User identity.
- Role.
- Expiration.


## 5. Standard Success Structure
A standard response may use:

{
    "data": {
      "id": 12,
      "title": "Python Fundamentals"
    }
}

Collection example:

{

    "data": [
      {
        "id": 12,
        "title": "Python Fundamentals"
      }
    ]
}


## 6. Standard Error Structure
All API errors should follow a consistent pattern:

{
    "error": "COURSE_NOT_FOUND",
    "message": "Course does not exist.",
    "details": null
}

Validation example:

{
    "error": "VALIDATION_ERROR",
    "message": "Request data is invalid.",
    "details": {
      "email": "A valid email address is required."
    }
}


## 7. Important HTTP Status Codes
    Code                      Meaning

    200     Successful request

    201     Resource created

    204     Successful request with no response body

    400     Invalid request

    401     Authentication missing/invalid

    403     Authenticated but not permitted

    404     Resource not found

    409    Conflict with existing state

    500    Unexpected server error

    503    Dependency/service temporarily
           unavailable


## 8. Authentication Endpoints
### 8.1 Register
POST /api/v1/auth/register

**Purpose**

Create a new Student or Instructor account.

Admin accounts cannot be created through public registration.

**Authentication**

Not required.

**Request**
{
    "name": "Aman Sharma",
    "email": "aman@example.com",
    "password": "StrongPassword123",
    "role": "STUDENT"
}

Allowed public roles:

STUDENT
INSTRUCTOR

**Success**
201 Created
{
  "data": {
   "id": 15,
   "name": "Aman Sharma",
   "email": "aman@example.com",
   "role": "STUDENT"

    }
}

Important Errors
400 INVALID_ROLE
400 VALIDATION_ERROR
409 EMAIL_ALREADY_REGISTERED


## 9. Login
POST /api/v1/auth/login

**Authentication**

Not required.

**Request**
{
    "email": "aman@example.com",
    "password": "StrongPassword123"
}

**Success**
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

**Errors**
401 INVALID_CREDENTIALS
403 ACCOUNT_DISABLED


## 10. Current User
GET /api/v1/auth/me

**Authentication**

Required.

**Allowed Roles**

All authenticated users.

**Success**
{
    "data": {
      "id": 15,
      "name": "Aman Sharma",
      "email": "aman@example.com",
      "role": "STUDENT"
    }
}


## 11. Logout
For stateless MVP JWT authentication, the frontend can discard the token.

An optional endpoint may be exposed as:

POST /api/v1/auth/logout

Server-side token revocation is not mandatory in the MVP.


## 12. Course Endpoints
### 12.1 List Published Courses
GET /api/v1/courses

**Authentication**

Not required.

**Purpose**

Return published Courses available for discovery.

**Success**
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

Draft Courses are excluded.


## 13. Get Course Details
GET /api/v1/courses/{course_id}

Published Course:

Publicly readable

Draft Course:

Readable only by owning Instructor

Possible Errors
404 COURSE_NOT_FOUND
403 COURSE_ACCESS_DENIED


## 14. Create Course
POST /api/v1/courses

**Authentication**

Required.

**Allowed Role**

INSTRUCTOR

**Request**
{
    "title": "Python Fundamentals",
    "description": "Complete introductory Python course."
}

**Success**
201 Created
{
  "data": {
    "id": 17,
    "title": "Python Fundamentals",
    "description": "Complete introductory Python course.",
    "status": "DRAFT",
    "instructor_id": 8
  }
}

**Errors**
400 VALIDATION_ERROR
401 AUTHENTICATION_REQUIRED
403 INSUFFICIENT_PERMISSION


## 15. Update Course
PUT /api/v1/courses/{course_id}

Allowed

Owning Instructor only.

**Request**
{
    "title": "Advanced Python Fundamentals",
    "description": "Updated course description."
}

**Errors**
403 NOT_COURSE_OWNER
404 COURSE_NOT_FOUND

## 16. Delete Course
DELETE /api/v1/courses/{course_id}

Reference rule:

- Owning Instructor.
- Course must be safe to delete.
- Published Course with learner history should not be destructively removed.

Possible response:

204 No Content

Possible conflict:

409 COURSE_HAS_LEARNER_DATA


## 17. Publish Course
PATCH /api/v1/courses/{course_id}/publish

Allowed

Owning Instructor.

**Success**
{
    "data": {
      "id": 17,
      "status": "PUBLISHED",
      "published_at": "2026-09-03T10:00:00Z"
    }
}


## 18. Instructor's Courses
GET /api/v1/instructor/courses

**Authentication**

Required.

Role
INSTRUCTOR

Returns both:

DRAFT
PUBLISHED

Courses owned by the Instructor.


## 19. Module Endpoints
List Modules
GET /api/v1/courses/{course_id}/modules

Published Course outline may be publicly visible.

Full restricted learning content remains controlled at Lesson level.


Create Module
POST /api/v1/courses/{course_id}/modules

Role

Owning Instructor.

**Request**
{
    "title": "Python Basics",
    "description": "Foundational Python concepts.",
    "position": 1
}

**Success**
201 Created


Update Module
PUT /api/v1/modules/{module_id}

Owning Instructor only.


Delete Module
DELETE /api/v1/modules/{module_id}

Owning Instructor only.

Deletion may be rejected if doing so would invalidate Student learning history.


## 20. Lesson Endpoints
List Lessons
GET /api/v1/modules/{module_id}/lessons

This may return lesson metadata.

Access to full lesson content follows Course access rules.


Create Lesson
POST /api/v1/modules/{module_id}/lessons

Role

Owning Instructor.

**Request**
{
    "title": "Python Variables",
    "content": "Lesson content...",
    "position": 1
}


Get Lesson
GET /api/v1/lessons/{lesson_id}

Allowed:

- Student enrolled in the Course.
- Owning Instructor.
- Admin where administrative access is required.

Unenrolled Student:

403 COURSE_ENROLLMENT_REQUIRED


Update Lesson
PUT /api/v1/lessons/{lesson_id}

Owning Instructor.


Delete Lesson
DELETE /api/v1/lessons/{lesson_id}

Owning Instructor, subject to learner-data restrictions.


## 21. Enrollment Endpoints
Enroll in Course
POST /api/v1/courses/{course_id}/enroll

**Authentication**

Required.

Role
STUDENT

Requirements

- Course exists.
- Course is published.
- Student is not already enrolled.

**Success**
201 Created

{
    "data": {
      "course_id": 15,
      "status": "ACTIVE",
      "message": "Enrollment successful."
    }
}

**Errors**
404 COURSE_NOT_FOUND
409 ALREADY_ENROLLED
403 COURSE_NOT_AVAILABLE


## 22. Student's Enrolled Courses
GET /api/v1/students/me/courses

Role

STUDENT.

**Success**
{
    "data": [
      {
        "course_id": 15,
        "title": "Python Fundamentals",
        "progress_percentage": 60
      }
    ]
}


## 23. View Enrolled Students
GET /api/v1/courses/{course_id}/students

Allowed:

- Owning Instructor.
- Admin.

## 24. Progress Endpoints
Complete Lesson
POST /api/v1/lessons/{lesson_id}/complete

Role

STUDENT.

Requirement

Student must be enrolled in the corresponding Course.

Behaviour

The operation is designed to be idempotent.

Submitting the same completion twice should not create duplicate LessonProgress rows.

**Success**
{
    "data": {
      "lesson_id": 22,
      "completed": true,
      "completed_at": "2026-09-03T10:30:00Z"
    }
}


## 25. Get Own Course Progress
GET /api/v1/courses/{course_id}/progress

Role

STUDENT.

Response
{
    "data": {
     "course_id": 8,
     "completed_lessons": 12,
     "total_lessons": 20,
     "progress_percentage": 60

    }
}


## 26. Instructor Views Student Progress
GET /api/v1/courses/{course_id}/students/{student_id}/progress

Allowed

Owning Instructor.

Response
{
    "data": {
      "student_id": 25,
      "course_id": 8,
      "completed_lessons": 12,
      "total_lessons": 20,
      "progress_percentage": 60
    }
}


## 27. Quiz Endpoints
Create Quiz
POST /api/v1/courses/{course_id}/quizzes

Role

Owning Instructor.

**Request**
{
    "title": "Python Basics Quiz",
    "description": "Assessment for Python fundamentals."
}


## 28. Get Quiz

GET /api/v1/quizzes/{quiz_id}

Student must be enrolled.

Student response must not expose:

is_correct
correct_answer

before submission.

Instructor response may include correct-answer information.


## 29. Example Student Quiz Response
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

Notice that this response does not contain:

"is_correct": true


## 30. Submit Quiz

POST /api/v1/quizzes/{quiz_id}/submit

Role

STUDENT.

Requirement

Student must be enrolled.

**Request**
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

Backend Performs
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

**Success**
201 Created
{
  "data": {
   "attempt_id": 95,

        "score": 80,
        "total_questions": 5,
        "correct_answers": 4
    }
}


## 31. Student Quiz Attempts
GET /api/v1/students/me/quiz-attempts

Optional filter:

GET /api/v1/students/me/quiz-attempts?course_id=12


## 32. Admin Endpoints
View Users
GET /api/v1/admin/users

Role

ADMIN.


View Courses
GET /api/v1/admin/courses

Role

ADMIN.

Returns both:

DRAFT
PUBLISHED

where administratively appropriate.

## 33. Optional Admin Endpoints
These are SHOULD HAVE, not mandatory MVP requirements.

PATCH /api/v1/admin/users/{user_id}/status

Example:

{
    "is_active": false
}

And:

PATCH /api/v1/admin/courses/{course_id}/status

for moderation.


## 34. AI Tutor Endpoint
POST /api/v1/ai/chat

Role

STUDENT.

**Authentication**

Required.

Authorization

Student must be enrolled in the requested Course.

**Request**
{
    "course_id": 12,
    "conversation_id": 35,
    "message": "Explain Python decorators in simple words."
}

For a new conversation:

conversation_id may be omitted/null

## 35. AI Chat Backend Flow
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


## 36. AI Chat Success Response
{
  "data": {
    "conversation_id": 35,
    "answer": "A Python decorator is a function that changes or extends the behaviour of
another function..."
  }
}


## 37. AI Chat Errors
401 AUTHENTICATION_REQUIRED

403 COURSE_ENROLLMENT_REQUIRED

404 COURSE_NOT_FOUND

404 CONVERSATION_NOT_FOUND

503 AI_SERVICE_UNAVAILABLE

A Student must not be allowed to provide someone else's conversation_id.


## 38. Optional AI Quiz Generator
POST /api/v1/ai/generate-quiz

Role

INSTRUCTOR.

Requirement

Instructor must own the Lesson's Course.

**Request**
{
    "lesson_id": 42,
    "difficulty": "medium",
    "number_of_questions": 5
}

Response
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

The response remains a draft.

It is not automatically stored or published.


## 39. Authorization Matrix
               Endpoint                        Public   Student    Instructor   Admin

 POST /auth/register                      Yes           —          —            No

 POST /auth/login                         Yes           Yes        Yes          Yes

 GET /auth/me                             No            Yes        Yes          Yes

 GET /courses                             Yes           Yes        Yes          Yes

 GET /courses/{id}                        Publishe      Yes        Yes          Yes
                                          d

 POST /courses                            No            No         Yes          No

 PUT /courses/{id}                        No            No         Owner        No

 PATCH /courses/{id}/publish              No            No         Owner        No

 DELETE /courses/{id}                     No            No         Owner        No

 POST /courses/{id}/modules               No            No         Owner        No

 POST /modules/{id}/lessons               No            No         Owner        No

 GET /lessons/{id}                        No            Enrolled   Owner        Yes

 POST /courses/{id}/enroll                No            Yes        No           No

 GET /students/me/courses                 No            Yes        No           No

 GET /courses/{id}/students               No            No         Owner        Yes

 POST /lessons/{id}/complete              No            Enrolled   No           No

 GET /courses/{id}/progress               No            Enrolled   No           No

 POST /courses/{id}/quizzes               No            No         Owner        No

 GET /quizzes/{id}                        No            Enrolled   Owner        Yes

 POST /quizzes/{id}/submit                No            Enrolled   No           No

GET                             No   Yes        No      No
/students/me/quiz-attempts

POST /ai/chat                   No   Enrolled   No      No

POST /ai/generate-quiz          No   No         Owner   No

GET /admin/users                No   No         No      Yes

GET /admin/courses              No   No         No      Yes


## 40. Core Error Codes
Suggested standardized codes:

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


## 41. Requirements Traceability Matrix
 Phase 1 Requirement             Database Entity          Primary API

User can register         User                     POST /auth/register

User can login            User                     POST /auth/login

Instructor creates        Course                   POST /courses
course

Instructor creates        Module                   POST
modules                                            /courses/{id}/modules

Instructor creates        Lesson                   POST
lessons                                            /modules/{id}/lessons

Student browses           Course                   GET /courses
courses

Student enrolls           Enrollment               POST /courses/{id}/enroll

Student views own         Enrollment + Course      GET /students/me/courses
courses

Student accesses          Lesson + Enrollment      GET /lessons/{id}
lesson

Student completes         LessonProgress           POST
lesson                                             /lessons/{id}/complete

Student views progress    LessonProgress           GET
                                                   /courses/{id}/progress

Instructor creates quiz   Quiz, Question,          POST
                          AnswerOption             /courses/{id}/quizzes

Student attempts quiz     QuizAttempt,             POST /quizzes/{id}/submit
                          StudentAnswer

 Student views results     QuizAttempt                  GET
                                                        /students/me/quiz-attempt
                                                        s

 Student asks AI           AIConversation,              POST /ai/chat
                           AIMessage

 Instructor generates AI   Lesson + AI Service          POST /ai/generate-quiz
 quiz

 Admin views users         User                         GET /admin/users

 Admin views courses       Course                       GET /admin/courses


## 42. API Design Principles
The API follows these rules:

## 1. Resource-oriented URLs.
## 2. Consistent /api/v1 prefix.
## 3. Appropriate HTTP methods.
## 4. JSON requests and responses.
## 5. Backend authorization.
## 6. Consistent error format.
## 7. Correct use of HTTP status codes.
## 8. No direct frontend-to-database access.
## 9. Correct answers hidden before Quiz submission.
   10.AI endpoints obey Course access rules.


---

## Phase 5 Integration Amendment — Course Quiz Listing

Phase 5 exposed an API-contract gap: the Course screen could retrieve an individual Quiz
with `GET /quizzes/{quiz_id}`, but it did not have a supported way to discover the Quiz IDs
belonging to a Course. Hard-coded Quiz IDs are not acceptable.

### GET `/api/v1/courses/{course_id}/quizzes`

**Purpose**

Return Quizzes belonging to a Course.

**Authentication**

Required.

**Authorization**

- Enrolled Student
- Owning Instructor
- Admin

**Example response**

```json
{
  "data": [
    {
      "id": 4,
      "course_id": 8,
      "title": "Python Basics Quiz",
      "description": "Assessment for Python fundamentals."
    }
  ]
}
```

**Errors**

- `401` — authentication missing or invalid
- `403` — insufficient permission or enrollment required
- `404` — Course not found

This amendment resolves the integration gap through the API contract instead of hard-coding
Quiz IDs in React.
