# SmartLMS — Phase 8 Production Verification Checklists

## Migration Checklist

- [ ] RDS database is reachable from backend.
- [ ] `alembic_version` exists.
- [ ] All historical migrations ran.
- [ ] Core LMS tables exist.
- [ ] AI tables exist.
- [ ] `course_chunks` exists.
- [ ] `vector` extension works where required.

## Environment Checklist

- [ ] `DATABASE_URL` points to RDS.
- [ ] `JWT_SECRET_KEY` is production-specific.
- [ ] `FRONTEND_ORIGIN` points to production frontend.
- [ ] AI provider key exists only on backend.
- [ ] LLM model is configured.
- [ ] Embedding model is configured.
- [ ] `VECTOR_STORE_TYPE=pgvector`.
- [ ] RAG configuration exists.
- [ ] No development-only secret is used.

## Instructor Smoke Test

```text
Instructor Login
    ↓
Create Draft Course
    ↓
Add Module
    ↓
Add Lesson
    ↓
Create / Generate Quiz
    ↓
Review
    ↓
Publish
```

## Student Smoke Test

```text
Student Login
    ↓
Browse
    ↓
Enroll
    ↓
Open Lesson
    ↓
Complete
    ↓
Attempt Quiz
    ↓
Progress
```

## AI Smoke Test

```text
Instructor → Generate AI Quiz
Student → Ask AI Tutor
```

Inspect:
- RDS data
- AI logs
- Tutor sources
