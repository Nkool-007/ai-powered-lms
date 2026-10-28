# Phase 6 AI API Demonstration

Base URL: `http://localhost:5000/api/v1`

## 1. Generate AI Quiz Draft

`POST /ai/generate-quiz`

Authorization: `Bearer <INSTRUCTOR_JWT>`

```json
{
  "lesson_id": 42,
  "difficulty": "medium",
  "number_of_questions": 5
}
```

Expected: structured draft only. No Quiz is persisted yet.

## 2. Rebuild Course AI Index

`POST /ai/courses/8/reindex`

Authorization: `Bearer <INSTRUCTOR_JWT>`

Expected example:

```json
{
  "data": {
    "course_id": 8,
    "chunks_indexed": 27
  }
}
```

## 3. Ask Course-Aware Tutor

`POST /ai/chat`

Authorization: `Bearer <STUDENT_JWT>`

```json
{
  "course_id": 8,
  "message": "Why does a JWT expire?",
  "conversation_id": null
}
```

Expected response contains `answer`, `sources`, `conversation_id`, and `insufficient_context`.

## 4. Negative Authorization Cases

- Student calls `/ai/generate-quiz` → 403.
- Instructor generates from another Instructor's Lesson → 403.
- Unenrolled Student calls `/ai/chat` → 403 `COURSE_ENROLLMENT_REQUIRED`.
- Invalid Lesson → 404.

## 5. Course Isolation Demonstration

Create Course A and Course B with clearly different Lesson content. Ask a question inside Course A and verify every retrieved source belongs to Course A.

## 6. Failure Demonstration

Simulate or explain:
- Provider unavailable → `AI_SERVICE_UNAVAILABLE`.
- Timeout → `AI_REQUEST_TIMEOUT`.
- Rate limit → `AI_RATE_LIMITED`.
- Malformed quiz JSON → `AI_INVALID_RESPONSE` and no Quiz saved.
- Empty retrieval → controlled Course-context response, not fabricated content.
