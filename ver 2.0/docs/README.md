# SmartLMS Documentation

This directory is the documentation source of truth through Phase 5.

## Phase 1 — Product Discovery, Requirements & Scope

- `PRD.md` — product overview, personas, user problems, goals, journeys, AI vision and success criteria.
- `user-stories.md` — prioritized Student, Instructor, Admin, AI/system and out-of-scope stories.
- `features.md` — feature catalogue classified by priority and MVP status.
- `scope.md` — mandatory MVP, optional capabilities, stretch goals and explicit exclusions.

Phase 1 defines **WHAT** the product should do and **WHY**.

## Phase 2 — Architecture, Database & API Design

- `architecture.md` — React/Flask/PostgreSQL/AI architecture, responsibilities, flows, authorization and failure boundaries.
- `database-design.md` — relational entities, keys, relationships, constraints, retention and migrations.
- `ER-diagram.png` — rendered entity relationship diagram.
- `ER-diagram.mmd` — Mermaid source.
- `ER-diagram.dot` — Graphviz source for the rendered PNG.
- `API-design.md` — REST API contract, authentication/authorization, error model and AI API boundary.

Phase 2 defines **HOW** the approved product is designed.

## Phase 5 — Full-Stack Integration

- `phase5-integration-test-plan.md` — manual end-to-end integration verification.
- `phase5-integration-notes.md` — integration defects, root causes, affected layers, solutions and final behaviour.

Phase 5 extends rather than replaces the earlier documentation.

### Phase 5 API Amendment

`API-design.md` includes:

```http
GET /api/v1/courses/{course_id}/quizzes
```

This lets an authorized client discover Course Quizzes without hard-coded IDs.

## Documentation Authority

```text
Phase 1 — Product Requirements & Scope
        ↓
Phase 2 — Architecture + Database + API Contract
        ↓
Phase 3 — Flask Backend
        ↓
Phase 4 — React Frontend
        ↓
Phase 5 — Full-Stack Integration
```

When documentation and implementation disagree, identify the mismatch and either fix the
implementation or deliberately update the contract.

## Phase Boundary

The Course-Aware AI Tutor remains the flagship AI capability in the product vision, but
Phase 5 does not implement RAG, embeddings, vector retrieval, AI Tutor logic or AI Quiz
generation. Those capabilities belong to the later AI phase.
