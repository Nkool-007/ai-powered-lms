# SmartLMS — AI Architecture & Design

## 1. AI Objectives

Phase 6 adds meaningful artificial intelligence to the existing SmartLMS.

The AI layer must enhance the existing LMS instead of operating as a disconnected chatbot.

The standard implementation contains:

1. AI Quiz Generator.
2. Course-Aware RAG Tutor.

An optional advanced implementation adds an application-state-aware Learning Agent.

The AI layer must obey the same authentication, authorization, Course ownership and Enrollment rules as the rest of SmartLMS.

## 2. AI Features

### AI Quiz Generator

An Instructor can generate draft multiple-choice Questions from a Lesson.

The AI receives:
- Lesson title.
- Lesson content.
- Difficulty.
- Requested number of Questions.

The generated Questions are treated as drafts.

Workflow:

```text
Lesson
↓
AI Generation
↓
Structured Draft
↓
Instructor Review
↓
Edit / Remove / Approve
↓
Existing Quiz System
```

AI never automatically publishes academic content.

### Course-Aware AI Tutor

An enrolled Student can ask questions about a Course.

The Tutor does not simply forward the question to an LLM.

```text
Student Question
↓
Question Embedding
↓
Vector Search
↓
course_id Filter
↓
Relevant Lesson Chunks
↓
Prompt Construction
↓
LLM
↓
Course-Aware Answer
↓
Lesson Sources
```

## 3. LLM Provider

The reference implementation uses an OpenAI-compatible backend provider.

Provider configuration is environment-driven. The provider is never called directly from React.

```text
React
↓
Flask
↓
AI Service
↓
Provider
```

This protects API credentials and keeps authorization under backend control.

## 4. AI Architecture

React is responsible for:
- Collecting Student questions.
- Displaying Tutor responses.
- Displaying sources.
- Collecting AI Quiz generation parameters.
- Displaying editable Quiz drafts.
- Showing loading and failure states.

Flask is responsible for:
- Authentication.
- Authorization.
- Course ownership.
- Enrollment checks.
- Prompt construction.
- Retrieval.
- LLM requests.
- Structured output validation.
- Conversation persistence.
- Failure handling.
- Cost/usage logging.

The LLM does not directly access PostgreSQL.

## 5. AI Quiz Generator

Endpoint:

`POST /api/v1/ai/generate-quiz`

Only the owning Instructor can generate Questions from a Lesson. The endpoint returns a draft. It does not create a production Quiz. The approved draft is later submitted through the existing Quiz API.

## 6. Human-in-the-Loop Workflow

AI-generated academic content must be reviewed by an Instructor.

```text
Lesson
↓
AI
↓
Draft
↓
Instructor Review
↓
Edit / Reject / Approve
↓
Save
```

The Instructor remains responsible for academic quality.

## 7. Quiz Structured Output

```json
{
  "questions": [
    {
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": 1,
      "explanation": "..."
    }
  ]
}
```

`correct_answer` is a zero-based array index. The backend validates the entire response before returning it as a usable draft.

## 8. RAG Architecture

RAG means Retrieval-Augmented Generation. Instead of asking the LLM to answer from general model knowledge alone, the application first retrieves relevant SmartLMS Course material.

```text
Question
↓
Retrieve Relevant Course Material
↓
Supply Retrieved Context to LLM
↓
Generate Answer
```

## 9. Course Indexing Pipeline

Published Lesson content is transformed into searchable vectors.

```text
Lesson
↓
Extract Text
↓
Clean
↓
Chunk
↓
Embedding
↓
Vector Store
```

The reference solution uses an explicit `POST /api/v1/ai/courses/{course_id}/reindex` operation controlled by the Course owner. A Course should be re-indexed after meaningful Lesson changes.

## 10. Chunking Strategy

Reference strategy:
- Approximately 220 words per chunk.
- Approximately 40 words of overlap.
- Empty chunks are discarded.

## 11. Embedding Strategy

Every Course chunk is converted into a numerical embedding. Student questions are converted using the same embedding model. Similarity between the question embedding and Course chunk embeddings is used to retrieve relevant learning material.

The embedding model is configured through `EMBEDDING_MODEL`.

## 12. Vector Store

The reference implementation uses PostgreSQL with pgvector because PostgreSQL already exists in SmartLMS, vector records can retain relational Course metadata, and `course_id` filtering can happen inside the retrieval query.

A CourseChunk stores:
- chunk_id
- course_id
- module_id
- lesson_id
- module_title
- lesson_title
- content
- content_hash
- embedding

## 13. Retrieval Strategy

For each Student question:
1. Create query embedding.
2. Filter CourseChunk records by `course_id`.
3. Rank matching chunks by cosine distance.
4. Select the top relevant chunks.
5. Reject low-relevance results using the configured threshold.
6. Pass only useful chunks to the Tutor prompt.

Reference configuration: `RAG_TOP_K=5`.

## 14. Course Isolation

Every retrieval query contains `course_id = requested_course`. Similarity alone is insufficient. This prevents Course material from another Course entering the prompt.

## 15. AI Tutor Prompt

The Tutor prompt contains:
- System instructions.
- Retrieved Course context.
- Recent conversation context where available.
- Student question.

If Course material does not support a Course-specific answer, the Tutor should not invent one.

## 16. Citations

Citations are generated from retrieved CourseChunk metadata rather than trusting the LLM to invent source names.

Example:

```json
{
  "answer": "...",
  "sources": [
    {
      "module_id": 4,
      "module_title": "Authentication",
      "lesson_id": 12,
      "lesson_title": "JWT Authentication"
    }
  ]
}
```

Raw embeddings are never returned to React.

## 17. Conversation Persistence

SmartLMS uses `AIConversation` and `AIMessage`. A conversation belongs to one Student and one Course. A Student cannot access another Student's conversation. Message roles are `USER` and `ASSISTANT`.

## 18. Optional Agent Tools

The advanced Learning Agent can use four controlled application tools:
- `search_course_content()`
- `get_student_progress()`
- `get_quiz_performance()`
- `get_course_structure()`

Tool access is derived from the authenticated User.

## 19. Failure Handling

Expected AI failures include:
- Provider unavailable.
- Provider rate limit.
- Timeout.
- Invalid JSON.
- Malformed structured output.
- Empty retrieval.
- Vector index not yet built.

The core LMS continues operating even when AI is unavailable.

## 20. Cost Awareness

Where available, SmartLMS records:
- AI feature.
- Model.
- Input tokens.
- Output tokens.
- Request latency.
- Success/failure status.

Secrets and complete private prompts are not written to normal application logs.

## 21. Environment Variables

```text
LLM_PROVIDER
OPENAI_API_KEY
LLM_MODEL
EMBEDDING_MODEL
VECTOR_STORE_TYPE
AI_REQUEST_TIMEOUT_SECONDS
RAG_TOP_K
RAG_MAX_COSINE_DISTANCE
RAG_CHUNK_WORDS
RAG_CHUNK_OVERLAP_WORDS
```

Real credentials are never committed.

## 22. AI API Contracts

### Generate Quiz
`POST /api/v1/ai/generate-quiz` — Instructor only.

### Rebuild Course AI Index
`POST /api/v1/ai/courses/{course_id}/reindex` — Owning Instructor only.

### AI Tutor
`POST /api/v1/ai/chat` — Student only.

### Conversations
`GET /api/v1/ai/conversations`

`GET /api/v1/ai/conversations/{conversation_id}`

Student can access only their own conversations.

## 23. Known Limitations

- Does not guarantee that every LLM answer is academically correct.
- Does not replace Instructor authority.
- Does not implement a production-scale recommendation engine.
- Does not implement a large multi-agent architecture.
- Requires re-indexing after Course content changes.
- Uses configurable semantic thresholds that may require tuning.
- Does not yet implement production monitoring or advanced AI security hardening.

## 24. Future Improvements

- Automatic background re-indexing.
- Streaming Tutor responses.
- Better document chunking.
- Hybrid keyword + vector search.
- Reranking.
- Personalized recommendations.
- Weak-area analysis.
- LangGraph workflow orchestration.
- LangSmith tracing.
- Advanced prompt-injection controls.
- Production AI observability.
