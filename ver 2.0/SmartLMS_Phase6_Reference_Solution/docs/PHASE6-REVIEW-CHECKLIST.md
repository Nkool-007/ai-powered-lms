# Phase 6 Review Checklist

## Core AI Architecture
- [ ] AI runs behind Flask.
- [ ] Provider credentials are environment-driven.
- [ ] No provider secret exists in React.
- [ ] Prompts are centralized.
- [ ] AI architecture is documented.

## AI Quiz Generator
- [ ] Instructor selects a Lesson.
- [ ] Lesson content is supplied to AI.
- [ ] Difficulty and question count are configurable.
- [ ] AI returns structured Questions.
- [ ] Backend validates output.
- [ ] Instructor previews/edits/removes Questions.
- [ ] Instructor explicitly approves.
- [ ] AI never auto-publishes.
- [ ] Approved Questions use the existing Quiz system.
- [ ] Unauthorized users are rejected.

## Course Indexing
- [ ] Published Lesson content can be indexed.
- [ ] Text cleaning works.
- [ ] Chunking and overlap work.
- [ ] Embeddings are stored.
- [ ] Metadata includes course_id/module_id/lesson_id.
- [ ] Re-indexing replaces stale Course vectors.

## Course-Aware RAG Tutor
- [ ] Student authenticates.
- [ ] Enrollment is required.
- [ ] Question is embedded.
- [ ] Retrieval filters by course_id.
- [ ] Cross-Course leakage is prevented.
- [ ] Relevant context reaches the LLM.
- [ ] Answer is Course-aware.
- [ ] Empty retrieval is handled.

## Citations
- [ ] Sources come from retrieval metadata.
- [ ] Sources identify Lesson information.
- [ ] Sources belong to current Course.
- [ ] Raw embeddings are not exposed to React.

## Failure Handling
- [ ] Provider unavailable handled.
- [ ] Rate limit handled.
- [ ] Timeout handled.
- [ ] Invalid JSON handled.
- [ ] Empty retrieval handled.
- [ ] Invalid Quiz data is not persisted.
- [ ] Core LMS survives AI failure.

## Cost Awareness
- [ ] Model can be identified.
- [ ] Request latency is measurable.
- [ ] Token usage logged where practical.
- [ ] Unnecessary Course context is not sent.
- [ ] Secrets are not logged.

## Frontend
- [ ] Instructor AI Quiz Generator uses real backend.
- [ ] Student AI Tutor uses real backend.
- [ ] Loading and error states work.
- [ ] Quiz preview works.
- [ ] Tutor sources display.

## Optional Agentic Extension
- [ ] Course content search tool.
- [ ] Student progress tool.
- [ ] Quiz performance tool.
- [ ] Course structure tool.
- [ ] Tools remain backend-authorized.
