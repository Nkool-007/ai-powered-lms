# AI-Powered LMS — Database Design

## 1. Database Overview

The AI-Powered LMS uses PostgreSQL as its primary relational database.

A relational database is appropriate because the system contains strongly connected entities.

Examples:

```text
Instructor → Course
Course → Module
Module → Lesson
Student → Enrollment → Course
Student → LessonProgress → Lesson
Quiz → Question → AnswerOption
Student → QuizAttempt → Quiz
```

The database must maintain:

- Referential integrity
- Unique constraints
- Relationships
- Consistent transactions
- Reliable historical data

SQLAlchemy will eventually be used as the ORM, with Alembic/Flask-Migrate managing schema migrations.

---

## 2. Naming Convention

Reference table names:

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
ai_conversations
ai_messages
```

Primary keys use:

```text
id
```

Foreign keys follow:

```text
<entity>_id
```

Examples:

```text
course_id
student_id
lesson_id
```

---

## 3. User Entity

### Purpose

Stores all platform users.

One table supports:

```text
STUDENT
INSTRUCTOR
ADMIN
```

rather than creating three independent account tables.

### Table: `users`

| Field | Logical Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| name | VARCHAR(120) | Yes | |
| email | VARCHAR(255) | Yes | UNIQUE |
| password_hash | VARCHAR(255) | Yes | |
| role | ENUM/String | Yes | STUDENT / INSTRUCTOR / ADMIN |
| is_active | BOOLEAN | Yes | Default TRUE |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

**Primary Key:** `users.id`

**Important Constraint:** `email UNIQUE`

Two accounts cannot use the same normalized email address.

---

## 4. User Deletion Decision

Users should generally not be physically deleted.

Instead:

```text
is_active = FALSE
```

Reasons:

- Historical enrollments remain valid
- Quiz attempts remain attributable
- Instructor-created courses remain linked
- AI conversation ownership remains intact

This represents a soft-deactivation strategy.

---

## 5. Course Entity

### Purpose

Represents a course created by an Instructor.

### Table: `courses`

| Field | Logical Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| title | VARCHAR(200) | Yes | |
| description | TEXT | Yes | |
| instructor_id | BIGINT | Yes | FK → users.id |
| status | ENUM/String | Yes | DRAFT / PUBLISHED |
| published_at | TIMESTAMP | No | |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

### Relationship

```text
User(INSTRUCTOR) 1 ───── * Course
```

Each Course has exactly one Instructor owner in the MVP.

One Instructor may own many Courses.

---

## 6. Course Ownership Decision

Multiple instructor ownership is **not supported in the MVP**.

Therefore:

```text
course.instructor_id
```

references one User.

Collaborative course ownership can be added later through another relationship entity if needed.

---

## 7. Module Entity

### Purpose

Represents a logical section inside a Course.

### Table: `modules`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| course_id | BIGINT | Yes | FK → courses.id |
| title | VARCHAR(200) | Yes | |
| description | TEXT | No | |
| position | INTEGER | Yes | |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

### Relationship

```text
Course 1 ───── * Module
```

Recommended ordering constraint:

```text
UNIQUE(course_id, position)
```

---

## 8. Lesson Entity

### Purpose

Represents one learning unit inside a Module.

### Table: `lessons`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| module_id | BIGINT | Yes | FK → modules.id |
| title | VARCHAR(200) | Yes | |
| content | TEXT | Yes | |
| position | INTEGER | Yes | |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

### Relationship

```text
Module 1 ───── * Lesson
```

Ordering:

```text
UNIQUE(module_id, position)
```

---

## 9. Enrollment Entity

### Purpose

Represents the relationship between Students and Courses.

A Student can enroll in many Courses.

A Course can contain many Students.

Therefore:

```text
Student * ───── * Course
```

This many-to-many relationship is resolved through:

```text
Enrollment
```

### Table: `enrollments`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| student_id | BIGINT | Yes | FK → users.id |
| course_id | BIGINT | Yes | FK → courses.id |
| status | ENUM/String | Yes | ACTIVE / COMPLETED |
| enrolled_at | TIMESTAMP | Yes | |
| completed_at | TIMESTAMP | No | |

### Critical Constraint

```text
UNIQUE(student_id, course_id)
```

This guarantees that a Student cannot enroll in the same Course twice.

---

## 10. Why Enrollment Is a Separate Entity

Incorrect design:

```text
Course
student_ids = [3, 7, 21, 24]
```

This creates problems with:

- Referential integrity
- Enrollment date
- Enrollment status
- Completion data
- Queries
- Duplicate prevention

Correct design:

```text
Student
    │
    ▼
Enrollment
    │
    ▼
Course
```

Enrollment itself contains meaningful information.

---

## 11. LessonProgress Entity

### Purpose

Stores lesson completion for individual Students.

### Table: `lesson_progress`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| student_id | BIGINT | Yes | FK → users.id |
| lesson_id | BIGINT | Yes | FK → lessons.id |
| completed | BOOLEAN | Yes | Default FALSE |
| completed_at | TIMESTAMP | No | |
| last_accessed_at | TIMESTAMP | No | |

### Constraint

```text
UNIQUE(student_id, lesson_id)
```

---

## 12. Why Progress Is Not Stored in Course

Incorrect:

```text
Course.progress = 60
```

Suppose:

```text
Aman → 60%
Neha → 25%
Rahul → 100%
```

There is no single Course progress value.

Progress belongs to:

```text
Student + Lesson
```

Course progress is calculated from individual lesson progress.

---

## 13. Progress Calculation

For one Student and one Course:

```text
number_of_completed_lessons
--------------------------- × 100
total_number_of_lessons
```

Example:

```text
12 / 20 × 100 = 60%
```

---

## 14. Quiz Entity

### Purpose

Represents an assessment belonging to a Course.

### Table: `quizzes`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| course_id | BIGINT | Yes | FK → courses.id |
| title | VARCHAR(200) | Yes | |
| description | TEXT | No | |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

### Relationship

```text
Course 1 ───── * Quiz
```

For the MVP, Quizzes belong directly to Courses.

Module-level or Lesson-level quizzes can be introduced later if required.

---

## 15. Question Entity

### Table: `questions`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| quiz_id | BIGINT | Yes | FK → quizzes.id |
| question_text | TEXT | Yes | |
| question_type | VARCHAR/ENUM | Yes | MCQ |
| position | INTEGER | Yes | |

### Relationship

```text
Quiz 1 ───── * Question
```

The MVP supports multiple-choice questions.

---

## 16. AnswerOption Entity

### Table: `answer_options`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| question_id | BIGINT | Yes | FK → questions.id |
| option_text | TEXT | Yes | |
| is_correct | BOOLEAN | Yes | |
| position | INTEGER | Yes | |

### Relationship

```text
Question 1 ───── * AnswerOption
```

Business rule:

> Each MVP MCQ should contain exactly one correct option.

This rule will primarily be validated by application logic.

---

## 17. QuizAttempt Entity

### Purpose

Represents one Student's attempt at one Quiz.

### Table: `quiz_attempts`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| quiz_id | BIGINT | Yes | FK → quizzes.id |
| student_id | BIGINT | Yes | FK → users.id |
| score | NUMERIC(5,2) | Yes | |
| started_at | TIMESTAMP | Yes | |
| submitted_at | TIMESTAMP | Yes | |

### Relationships

```text
Student 1 ───── * QuizAttempt
Quiz 1 ───── * QuizAttempt
```

---

## 18. Quiz Attempt Decision

Multiple attempts are permitted.

Therefore, there is deliberately **no** unique constraint on:

```text
(student_id, quiz_id)
```

Example:

```text
Student 15
Quiz 9

Attempt 1 → 55%
Attempt 2 → 75%
Attempt 3 → 90%
```

Each attempt remains independently stored.

---

## 19. StudentAnswer Entity

### Purpose

Stores the selected answer for each Question in an attempt.

### Table: `student_answers`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| quiz_attempt_id | BIGINT | Yes | FK → quiz_attempts.id |
| question_id | BIGINT | Yes | FK → questions.id |
| selected_option_id | BIGINT | Yes | FK → answer_options.id |
| is_correct | BOOLEAN | Yes | |

### Constraint

```text
UNIQUE(quiz_attempt_id, question_id)
```

One Question should have one submitted answer per attempt.

---

## 20. Why Store `is_correct`?

Although correctness can initially be derived from `AnswerOption.is_correct`, the result is stored as an attempt-time snapshot.

This helps preserve historical result integrity.

If an Instructor later corrects a Question, an old QuizAttempt should not silently change from 70% to 80% without an explicit regrading process.

---

## 21. AIConversation Entity

### Purpose

Represents one AI Tutor conversation between one Student and the system within one Course.

### Table: `ai_conversations`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| student_id | BIGINT | Yes | FK → users.id |
| course_id | BIGINT | Yes | FK → courses.id |
| created_at | TIMESTAMP | Yes | |
| updated_at | TIMESTAMP | Yes | |

### Relationships

```text
Student 1 ───── * AIConversation
Course 1 ───── * AIConversation
```

---

## 22. Why AIConversation Contains `course_id`

The AI Tutor is **course-aware**.

A conversation about Python Full Stack should not accidentally retrieve content from Java Programming.

Associating the conversation with Course allows:

- Course-specific retrieval
- Authorization checks
- Better context
- Conversation organization

---

## 23. AIMessage Entity

### Table: `ai_messages`

| Field | Type | Required | Constraint |
|---|---|---:|---|
| id | BIGINT | Yes | PK |
| conversation_id | BIGINT | Yes | FK → ai_conversations.id |
| role | ENUM/String | Yes | USER / ASSISTANT |
| content | TEXT | Yes | |
| created_at | TIMESTAMP | Yes | |

### Relationship

```text
AIConversation 1 ───── * AIMessage
```

---

## 24. Vector Store Data

Vector data is treated as AI infrastructure rather than part of the core transactional ER model.

A future vector record will conceptually contain:

```text
chunk_id
course_id
module_id
lesson_id
content
embedding
```

The critical metadata is:

```text
course_id
```

because retrieval must be course-scoped.

---

## 25. Relationship Summary

### One-to-Many

```text
Instructor(User) 1 ───── * Course
Course 1 ───── * Module
Module 1 ───── * Lesson
Course 1 ───── * Quiz
Quiz 1 ───── * Question
Question 1 ───── * AnswerOption
Student(User) 1 ───── * Enrollment
Course 1 ───── * Enrollment
Student(User) 1 ───── * LessonProgress
Lesson 1 ───── * LessonProgress
Student(User) 1 ───── * QuizAttempt
Quiz 1 ───── * QuizAttempt
QuizAttempt 1 ───── * StudentAnswer
Student(User) 1 ───── * AIConversation
Course 1 ───── * AIConversation
AIConversation 1 ───── * AIMessage
```

---

## 26. Many-to-Many

Conceptually:

```text
Student * ───── * Course
```

Implementation:

```text
Student
   │
   ▼
Enrollment
   │
   ▼
Course
```

---

## 27. One-to-One Relationships

No mandatory one-to-one relationship is required in the MVP.

---

## 28. Foreign Key Summary

```text
courses.instructor_id → users.id
modules.course_id → courses.id
lessons.module_id → modules.id
enrollments.student_id → users.id
enrollments.course_id → courses.id
lesson_progress.student_id → users.id
lesson_progress.lesson_id → lessons.id
quizzes.course_id → courses.id
questions.quiz_id → quizzes.id
answer_options.question_id → questions.id
quiz_attempts.quiz_id → quizzes.id
quiz_attempts.student_id → users.id
student_answers.quiz_attempt_id → quiz_attempts.id
student_answers.question_id → questions.id
student_answers.selected_option_id → answer_options.id
ai_conversations.student_id → users.id
ai_conversations.course_id → courses.id
ai_messages.conversation_id → ai_conversations.id
```

---

## 29. Important Unique Constraints

### User Email

```text
UNIQUE(email)
```

### Enrollment

```text
UNIQUE(student_id, course_id)
```

### Lesson Progress

```text
UNIQUE(student_id, lesson_id)
```

### Student Answer

```text
UNIQUE(quiz_attempt_id, question_id)
```

### Module Ordering

```text
UNIQUE(course_id, position)
```

### Lesson Ordering

```text
UNIQUE(module_id, position)
```

---

## 30. Referential Integrity

The following should never exist independently:

```text
Module without Course
Lesson without Module
Question without Quiz
AnswerOption without Question
StudentAnswer without QuizAttempt
AIMessage without AIConversation
```

Foreign keys enforce these relationships.

---

## 31. Delete and Retention Decisions

### Users

Use:

```text
is_active = FALSE
```

rather than deleting the User.

### Courses

A draft Course with no learner data may be permanently deleted by its Instructor.

For a published Course, prefer:

```text
Unpublish
```

rather than destructive deletion after Student activity exists.

This protects historical:

- Enrollments
- Quiz attempts
- Progress

### Modules and Lessons

Deletion may be allowed while a Course is still being authored.

Once meaningful Student progress exists, destructive deletion should be restricted to avoid corrupting learner history.

### Enrollment

The MVP does not require Student unenrollment.

Enrollment records should therefore normally be retained.

### Quiz Attempts

QuizAttempts and StudentAnswers should be retained as learning history.

### AI Conversations

Students may later be allowed to delete conversations, but this is outside the mandatory Phase 2 database requirement.

---

## 32. Database Migration Strategy

Schema evolution should occur incrementally.

### Migration 001

```text
Create users
```

### Migration 002

```text
Create courses
Add instructor relationship
```

### Migration 003

```text
Create modules
Create lessons
```

### Migration 004

```text
Create enrollments
Add UNIQUE(student_id, course_id)
```

### Migration 005

```text
Create quizzes
Create questions
Create answer_options
```

### Migration 006

```text
Create lesson_progress
Add UNIQUE(student_id, lesson_id)
```

### Migration 007

```text
Create quiz_attempts
Create student_answers
```

### Migration 008

```text
Create ai_conversations
Create ai_messages
```

Vector infrastructure can be introduced later during the AI implementation phase.

---

## 33. Data Design Principles

1. Avoid duplicated data.
2. Use Foreign Keys for relationships.
3. Use constraints for important rules.
4. Do not store arrays of relational IDs when a proper relationship is required.
5. Progress belongs to individual learners.
6. Historical quiz attempts should remain stable.
7. AI conversations are Student- and Course-specific.
8. Core transactional data remains independent of AI provider availability.
