# SmartLMS Backend Demonstration

Base URL:

```text
http://localhost:5000/api/v1
```

## Instructor Flow

1. `GET /health`
2. `POST /auth/register` as `INSTRUCTOR`
3. `POST /auth/login` and save the access token
4. `POST /courses`
5. `POST /courses/{course_id}/modules`
6. `POST /modules/{module_id}/lessons`
7. `POST /courses/{course_id}/quizzes`
8. `PATCH /courses/{course_id}/publish`

## Student Flow

9. `POST /auth/register` as `STUDENT`
10. `POST /auth/login`
11. `GET /courses`
12. `POST /courses/{course_id}/enroll`
13. Repeat enrollment and verify `409 ALREADY_ENROLLED`
14. `GET /students/me/courses`
15. `GET /lessons/{lesson_id}`
16. `POST /lessons/{lesson_id}/complete`
17. Repeat completion and verify no duplicate progress row
18. `GET /courses/{course_id}/progress`
19. `GET /courses/{course_id}/quizzes`
20. `GET /quizzes/{quiz_id}` and verify student payload contains no `is_correct`
21. `POST /quizzes/{quiz_id}/submit`
22. `GET /students/me/quiz-attempts`

## Mandatory Negative Checks

- `/auth/me` without a token -> `401 AUTHENTICATION_REQUIRED`
- Student creates a Course -> `403 INSUFFICIENT_PERMISSION`
- Instructor B edits Instructor A's Course -> `403 NOT_COURSE_OWNER`
- Unenrolled Student opens restricted Lesson -> `403 COURSE_ENROLLMENT_REQUIRED`
- Invalid Quiz answer -> `400 INVALID_QUIZ_SUBMISSION`
- Expired token -> `401 TOKEN_EXPIRED`

## Example Quiz Creation Payload

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
        }
      ]
    }
  ]
}
```

## Example Quiz Submission

```json
{
  "answers": [
    {
      "question_id": 1,
      "selected_option_id": 2
    }
  ]
}
```
