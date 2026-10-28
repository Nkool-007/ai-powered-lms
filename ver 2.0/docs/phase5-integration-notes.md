# SmartLMS — Phase 5 Integration Notes

## 1. Purpose

This document records important problems discovered while connecting the Phase 4 React
frontend to the Phase 3 Flask/PostgreSQL backend.

Integration problems should be solved at the correct architectural layer rather than hidden
using frontend workarounds.

---

## Issue 1 — Browser Requests Blocked by CORS

## Observed Behaviour

The Flask APIs worked through Postman.

The same requests from:

http://localhost:5173

failed in the browser.

## Root Cause

React and Flask run on different origins.

React:

http://localhost:5173

Flask:

http://localhost:5000

The browser therefore applies CORS rules.

## Affected Layer

Backend configuration.

## Solution

Added Flask-Cors.

Added:

FRONTEND_ORIGIN=http://localhost:5173

Configured `/api/*` to allow the approved origin and Authorization header.

## Final Behaviour

React successfully communicates with the Flask API.

---

## Issue 2 — JWT Header Logic Was Distributed

## Observed Behaviour

Protected endpoints require:

Authorization: Bearer <JWT>

Adding this manually to every request would create repeated code and inconsistent
behaviour.

## Root Cause

Authentication-header responsibility was not sufficiently centralized.

## Affected Layer

Frontend services.

## Solution

The Axios instance in:

frontend/src/services/api.js

now uses a request interceptor.

Every request automatically reads the stored JWT and adds:

Authorization: Bearer <JWT>

when a token exists.

## Final Behaviour

Pages and individual services no longer manually construct authentication headers.

---

## Issue 3 — Expired JWT Left Stale Frontend Session

## Observed Behaviour

A User could appear logged in inside React after the JWT had expired.

Protected API requests then failed with 401.

## Root Cause

The Phase 4 frontend restored authentication state but did not centrally react to every 401
returned after session expiration.

## Affected Layer

Frontend authentication lifecycle.

## Solution

Added an Axios response interceptor.

When:

HTTP 401

occurs while a token exists:

1. Token is removed.
2. `smartlms:auth-expired` event is dispatched.
3. AuthContext clears User state.
4. ProtectedRoute redirects unauthenticated users.

## Final Behaviour

Expired sessions transition predictably back to the unauthenticated state.

---

## Issue 4 — JWT Error Structures Were Inconsistent

## Observed Behaviour

Application-generated errors used:

{
    "error": "...",
    "message": "...",
    "details": null
}

JWT-library failures could return a different shape.

## Root Cause

Flask-JWT-Extended default error responses did not necessarily use the application's
response convention.

## Affected Layer

Backend authentication.

## Solution

Configured:

- unauthorized_loader
- invalid_token_loader
- expired_token_loader
- revoked_token_loader

to use the common error response utility.

## Final Behaviour

Authentication failures have predictable machine-readable codes.

---

## Issue 5 — Raw Axios Errors Could Reach Users

## Observed Behaviour

A failed request could potentially display:

AxiosError: Request failed with status code 401

## Root Cause

Error extraction was not comprehensive enough.

## Affected Layer

Frontend utility layer.

## Solution

Updated:

frontend/src/utils/errors.js

to handle:

- backend messages
- backend codes
- network failure
- timeout
- fallback message

## Final Behaviour

Users receive understandable application messages.

---

## Issue 6 — Course Could Not Reliably Discover Quiz IDs

## Observed Behaviour

The backend could retrieve:

GET /quizzes/{quiz_id}

but the frontend did not have a supported API to ask:

"What Quizzes belong to this Course?"

## Root Cause

A Course-level Quiz listing operation was missing from the API contract.

## Incorrect Workaround

Hard-code:

const quizId = 1;

## Solution

Added:

GET /api/v1/courses/{course_id}/quizzes

Authorization:

- enrolled Student
- Course owner
- Admin

Updated:

docs/API-design.md

and:

frontend/src/services/quizService.js

## Final Behaviour

Students can discover available Course Quizzes using the actual backend relationship.

---

## Issue 7 — 401 and 403 Required Different Frontend Behaviour

## Observed Behaviour

Treating every authorization-related failure as a logout would produce incorrect behaviour.

## Root Cause

401 and 403 represent different states.

401:

Not correctly authenticated.

403:

Authenticated but not authorized.

## Solution

401 with an existing token:

Clear invalid session.

403:

Keep User logged in and display permission error/Forbidden page where appropriate.

## Final Behaviour

Authentication and authorization failures are handled correctly.

---

## Issue 8 — Network Failure Needed a Defined UI State

## Observed Behaviour

If the Flask server was unavailable, the frontend could otherwise expose a raw network
error.

## Root Cause

Network errors have no normal backend response payload.

## Solution

The shared error utility detects:

error.request && !error.response

and displays:

"Unable to connect to the server."

## Final Behaviour

Network failure enters a predictable error state.

---

## Issue 9 — Request Timeout Needed Handling

## Observed Behaviour

Slow/unavailable API calls could otherwise make the UI appear stuck.

## Solution

Axios timeout:

10000 ms

The common error utility maps ECONNABORTED to:

"The request timed out. Please try again."

## Final Behaviour

The UI exits its loading state and reports the failure.

---

## Issue 10 — Date Display Required Consistency

## Observed Behaviour

Backend timestamps are machine-friendly ISO values.

Example:

2026-10-27T10:15:30+00:00

Displaying these directly is not ideal for users.

## Solution

Added:

frontend/src/utils/date.js

using:

Intl.DateTimeFormat

## Final Behaviour

Dates are displayed in a human-readable localized format while the API remains
machine-friendly.

---

## Issue 11 — Backend Authorization Remains Authoritative

## Observation

React hides Instructor screens from Students.

However, users can manually call APIs.

## Decision

No security decision depends on React navigation.

Flask continues to verify:

- JWT
- User role
- Course ownership
- Enrollment
- Resource existence

## Final Behaviour

React improves UX.

Flask enforces security.

---

## Issue 12 — Core Mock Data Removed

## Problem

Phase 4 UI development may use temporary fixtures.

## Phase 5 Rule

Core workflows must now use real API responses.

## Solution

Production pages retrieve data through:

authService

courseService

enrollmentService

quizService

## Final Behaviour

Browser refresh reloads persistent information from PostgreSQL rather than recreating
temporary frontend objects.

---

# Final Integration State

The application now supports:

Instructor:

Login
→ Create Course
→ Add Module
→ Add Lesson
→ Create Quiz
→ Publish
→ View Students
→ View Progress

Student:

Register/Login

→ Browse
→ Enroll
→ My Courses
→ View Lesson
→ Complete Lesson
→ Track Progress
→ Attempt Quiz
→ View Result

Core application state persists through the backend and PostgreSQL.

Phase 5 is therefore ready for the Core Product Review.
