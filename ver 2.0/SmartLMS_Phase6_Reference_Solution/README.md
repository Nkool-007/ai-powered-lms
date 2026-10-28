# SmartLMS — Phase 6 Reference Solution Overlay

This folder contains the Phase 6 AI/Agentic System reference deliverables to merge into the working Phase 5 SmartLMS repository.

## Project Status

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Product Discovery, Requirements & Scope | Complete |
| Phase 2 | Architecture, Database & API Design | Complete |
| Phase 3 | Flask REST Backend | Complete |
| Phase 4 | React Frontend | Complete |
| Phase 5 | Full-Stack Integration | Complete |
| Phase 6 | AI / Agentic System | Complete |
| Phase 7 | DevOps / Dockerisation | Next |

## AI Intelligence Layer

Phase 6 adds two standard AI capabilities:

1. AI Quiz Generator.
2. Course-Aware RAG Tutor.

An optional Learning Agent uses authenticated LMS application state.

### AI Provider

The provider is configured through backend environment variables. Provider credentials never exist in React source code.

### AI Quiz Generator

```text
Lesson
↓
Generate With AI
↓
Structured Draft
↓
Instructor Review
↓
Edit / Reject / Approve
↓
Existing Quiz System
```

AI-generated Questions are never automatically published.

### Course-Aware Tutor

```text
Question
↓
Embedding
↓
Vector Search
↓
course_id Filter
↓
Relevant Lesson Chunks
↓
LLM
↓
Course-Aware Answer
↓
Sources
```

### Vector Store

The reference implementation uses PostgreSQL with pgvector. Each Course chunk retains Course, Module and Lesson metadata alongside the chunk text and embedding.

### Authorization

- AI Quiz Generator: owning Instructor only.
- AI Tutor: authenticated Student with active Course Enrollment.
- AI tools cannot bypass Flask authorization.

### AI APIs

- `POST /api/v1/ai/generate-quiz`
- `POST /api/v1/ai/courses/{course_id}/reindex`
- `POST /api/v1/ai/chat`
- `GET /api/v1/ai/conversations`
- `GET /api/v1/ai/conversations/{conversation_id}`

### Environment Variables

- `LLM_PROVIDER`
- `OPENAI_API_KEY`
- `LLM_MODEL`
- `EMBEDDING_MODEL`
- `VECTOR_STORE_TYPE`
- `AI_REQUEST_TIMEOUT_SECONDS`
- `RAG_TOP_K`
- `RAG_MAX_COSINE_DISTANCE`
- `RAG_CHUNK_WORDS`
- `RAG_CHUNK_OVERLAP_WORDS`

Real credentials must never be committed.

### AI Failure Handling

The application handles provider unavailability, rate limits, timeouts, invalid JSON, malformed structured output and empty retrieval. Failure of the AI provider does not prevent normal LMS use.

### Human Review

AI-generated educational content is draft content until reviewed and approved by an Instructor.

### Optional Agentic Extension

The Learning Agent may use Course content search, Student progress, Quiz performance and Course structure. Tool calls remain restricted to data permitted for the authenticated Student.

## Important Integration Note

This package is a Phase 6 overlay, not a replacement for Phases 1–5. See `MERGE-INSTRUCTIONS.md` before copying files into the existing repository.
