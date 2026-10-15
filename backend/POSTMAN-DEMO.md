# Phase 3 Backend API Demonstration

Base URL:

```text
http://localhost:5000/api/v1
```

## 1. Health Check

```http
GET /health
```

Expected:

```text
200 OK
```

```json
{
  "status": "ok"
}
```

## 2. Register Instructor

```http
POST /auth/register
```

```json
{
  "name": "Nina Instructor",
  "email": "nina@example.com",
  "password": "Instructor123",
  "role": "INSTRUCTOR"
}
```

Expected: `201 Created`

## 3. Login Instructor

```http
POST /auth/login
```

```json
{
  "email": "nina@example.com",
  "password": "Instructor123"
}
```

Save `access_token` as `INSTRUCTOR_TOKEN`.

## 4. Create Course

```http
POST /courses
Authorization: Bearer {{INSTRUCTOR_TOKEN}}
```

```json
{
  "title": "Python Fundamentals",
  "description": "Learn Python from first principles."
}
```

Expected: `201 Created`

Save the Course ID.

## 5. Create Module

```http
POST /courses/{{COURSE_ID}}/modules
Authorization: Bearer {{INSTRUCTOR_TOKEN}}
```

```json
{
  "title": "Python Basics",
  "description": "Core Python concepts",
  "position": 1
}
```

Save the Module ID.

## 6. Create Lesson

```http
POST /modules/{{MODULE_ID}}/lessons
Authorization: Bearer {{INSTRUCTOR_TOKEN}}
```

```json
{
  "title": "Python Variables",
  "content": "Variables store references to values.",
  "position": 1
}
```

Save the Lesson ID.

## 7. Create Quiz

```http
POST /courses/{{COURSE_ID}}/quizzes
Authorization: Bearer {{INSTRUCTOR_TOKEN}}
```

```json
{
  "title": "Python Basics Quiz",
  "description": "Test Python fundamentals.",
  "questions": [
    {
      "question_text": "Which keyword defines a Python function?",
      "position": 1,
      "options": [
        {
          "option_text": "function",
          "position": 1,
          "is_correct": false
        },
        {
          "option_text": "def",
          "position": 2,
          "is_correct": true
        },
        {
          "option_text": "func",
          "position": 3,
          "is_correct": false
        },
        {
          "option_text": "define",
          "position": 4,
          "is_correct": false
        }
      ]
    }
  ]
}
```

Save the Quiz ID, Question ID, and option IDs from the Instructor response.

## 8. Publish Course

```http
PATCH /courses/{{COURSE_ID}}/publish
Authorization: Bearer {{INSTRUCTOR_TOKEN}}
```

Expected: `200 OK` and `status = PUBLISHED`.

## 9. Register Student

```http
POST /auth/register
```

```json
{
  "name": "Aman Student",
  "email": "aman@example.com",
  "password": "Student123",
  "role": "STUDENT"
}
```

## 10. Login Student

```http
POST /auth/login
```

```json
{
  "email": "aman@example.com",
  "password": "Student123"
}
```

Save the token as `STUDENT_TOKEN`.

## 11. Browse Courses

```http
GET /courses
```

Expected: `Python Fundamentals` appears.

## 12. Student Attempts Course Creation

```http
POST /courses
Authorization: Bearer {{STUDENT_TOKEN}}
```

Expected: `403 Forbidden`.

## 13. Enroll

```http
POST /courses/{{COURSE_ID}}/enroll
Authorization: Bearer {{STUDENT_TOKEN}}
```

Expected: `201 Created`.

## 14. Duplicate Enrollment

Repeat:

```http
POST /courses/{{COURSE_ID}}/enroll
```

Expected:

```text
409 Conflict
ALREADY_ENROLLED
```

## 15. Access Lesson

```http
GET /lessons/{{LESSON_ID}}
Authorization: Bearer {{STUDENT_TOKEN}}
```

Expected: `200 OK`.

## 16. Complete Lesson

```http
POST /lessons/{{LESSON_ID}}/complete
Authorization: Bearer {{STUDENT_TOKEN}}
```

Expected: `200 OK`.

## 17. Complete Same Lesson Again

Repeat the previous request.

Expected: `200 OK`.

No second `LessonProgress` row should be created.

## 18. View Progress

```http
GET /courses/{{COURSE_ID}}/progress
Authorization: Bearer {{STUDENT_TOKEN}}
```

Example:

```json
{
  "data": {
    "course_id": 1,
    "completed_lessons": 1,
    "total_lessons": 1,
    "progress_percentage": 100
  }
}
```

## 19. Retrieve Quiz

```http
GET /quizzes/{{QUIZ_ID}}
Authorization: Bearer {{STUDENT_TOKEN}}
```

Verify that the Student response does **not** contain:

```text
is_correct
correct_answer
```

## 20. Submit Quiz

Use the real IDs returned by the Create Quiz API.

```http
POST /quizzes/{{QUIZ_ID}}/submit
Authorization: Bearer {{STUDENT_TOKEN}}
```

```json
{
  "answers": [
    {
      "question_id": "{{QUESTION_ID}}",
      "selected_option_id": "{{CORRECT_OPTION_ID}}"
    }
  ]
}
```

Expected: `201 Created`.

Example:

```json
{
  "data": {
    "attempt_id": 1,
    "score": 100.0,
    "total_questions": 1,
    "correct_answers": 1
  }
}
```

## 21. View Quiz Attempts

```http
GET /students/me/quiz-attempts
Authorization: Bearer {{STUDENT_TOKEN}}
```

Expected: the stored attempt is returned.

# Mandatory Negative Tests

## Missing JWT

```http
GET /auth/me
```

Expected: `401 Unauthorized`.

## Student Creates Course

```http
POST /courses
```

Use Student token.

Expected: `403 Forbidden`.

## Duplicate Enrollment

Call:

```http
POST /courses/{id}/enroll
```

twice.

Expected second response: `409 Conflict`.

## Unenrolled Student Accesses Lesson

Use another Student account that is not enrolled:

```http
GET /lessons/{lesson_id}
```

Expected: `403 Forbidden`.

## Instructor Attempts to Edit Another Instructor's Course

Create Instructor B.

Use Instructor B's JWT:

```http
PUT /courses/{course-owned-by-instructor-A}
```

Expected: `403 Forbidden`.
