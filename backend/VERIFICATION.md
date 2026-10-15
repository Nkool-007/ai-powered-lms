# Phase 3 Reference Verification

## Expected Tables After Migration

```text
users
courses
modules
lessons
enrollments
lesson_progress
quizzes
questions
answer_options
quiz_attempts
student_answers
alembic_version
```

## PostgreSQL Table Check

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

## Duplicate Enrollment Check

```sql
SELECT
    student_id,
    course_id,
    COUNT(*)
FROM enrollments
GROUP BY
    student_id,
    course_id
HAVING COUNT(*) > 1;
```

Expected: `0 rows`.

## Progress Verification

```sql
SELECT
    student_id,
    lesson_id,
    completed,
    completed_at
FROM lesson_progress;
```

There should be only one row for each `student_id + lesson_id`.

## Quiz Attempt Verification

```sql
SELECT
    id,
    quiz_id,
    student_id,
    score,
    submitted_at
FROM quiz_attempts
ORDER BY submitted_at DESC;
```

Then:

```sql
SELECT
    quiz_attempt_id,
    question_id,
    selected_option_id,
    is_correct
FROM student_answers;
```

This demonstrates that a final score is backed by persisted StudentAnswers.
