# How to Apply This Phase 6 Reference Solution

This package corresponds to the Phase 6 reference solution and assumes the Phase 5 SmartLMS is already working.

## Copy New Files

Copy these new areas directly:

- `backend/app/ai/`
- `backend/app/models/ai.py`
- `backend/app/routes/ai.py`
- `frontend/src/services/aiService.js`
- `frontend/src/pages/instructor/AIQuizGenerator.jsx`
- `frontend/src/pages/student/AITutor.jsx`
- `frontend/src/components/ai/AIIndexButton.jsx`
- `docs/AI-design.md`

## Merge Existing Files — Do Not Blindly Overwrite

The Phase 6 document says to extend existing Phase 5 files. The package therefore provides merge snippets for:

- `backend/app/config.py` → `backend/app/config.phase6-snippet.py`
- `backend/app/models/__init__.py` → `backend/app/models/__init__.phase6-snippet.py`
- `backend/app/routes/__init__.py` → `backend/app/routes/__init__.phase6-snippet.py`
- `frontend/src/App.jsx` → instructions in `frontend/PHASE6-ROUTES.md`

`backend/requirements.txt` and `backend/.env.example` show the reference merged dependency/configuration state.

## Database Migration

`backend/migrations/versions/009_add_pgvector_course_chunks.py` follows the conceptual Phase 6 sequence from the reference solution. If your repository uses generated Alembic revision hashes, replace the `revision` and `down_revision` values with IDs from your actual migration history.

If `AIConversation` and `AIMessage` already exist from an earlier migration, do not create them again. The Phase 6 model file activates them for use; the provided migration focuses on pgvector/course chunks.

## Model Base Helper

The reference code imports `TimestampMixin` from `app.models.base`. A small compatibility implementation is included at `backend/app/models/base.py`. If the Phase 5 repository already has a base/mixin implementation, retain the existing one rather than overwriting it.

## Apply Environment Configuration

Copy the AI variable names from `backend/.env.example` into the real local `.env`, and provide actual values only locally. Never commit credentials.

## Phase 6 Run Order

1. Merge the files.
2. Install backend dependencies.
3. Configure the AI environment variables.
4. Ensure PostgreSQL has pgvector support.
5. Run the migration.
6. Start Flask and React.
7. Publish a Course with Lessons.
8. Rebuild that Course's AI index.
9. Demonstrate the AI Quiz Generator.
10. Demonstrate the enrolled Student RAG Tutor.
11. Demonstrate Course isolation and failure handling.

## What This Package Does Not Include

It does not duplicate the complete Phase 1–5 backend/frontend because Phase 6 extends that existing implementation. Existing models, services, components, authorization helpers, response helpers, Quiz APIs and LMS screens must remain in place.
