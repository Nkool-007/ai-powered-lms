# Phase 3 Reference Migration Plan

The Phase 3 assignment requires actual migration history instead of relying on `db.create_all()` for production schema management.

Recommended evolution:

1. `001_create_users`
2. `002_create_courses`
3. `003_create_modules_and_lessons`
4. `004_create_enrollments`
5. `005_create_quizzes_questions_options`
6. `006_create_lesson_progress`
7. `007_create_quiz_attempts_student_answers`

The reference package includes working example revision files using simple reference IDs (`001` through `007`).

In a student's own repository, Flask-Migrate/Alembic will normally generate different revision IDs. Do not copy revision IDs blindly into an existing migration history.

## Typical workflow

Initialize migrations once:

```bash
flask --app run.py db init
```

Generate changes as models evolve:

```bash
flask --app run.py db migrate -m "create users"
flask --app run.py db upgrade
```

At the end, verify a fresh database can be reconstructed:

```bash
flask --app run.py db upgrade
flask --app run.py db current
flask --app run.py db history
```
