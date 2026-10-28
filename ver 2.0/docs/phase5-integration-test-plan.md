# SmartLMS — Phase 5 Integration Test Plan

## 1. Purpose

This document verifies that the React frontend, Flask REST API, SQLAlchemy application
layer, and PostgreSQL database operate together as one complete LMS.

The purpose is not merely to prove that individual endpoints work.

The objective is to prove:

React
→ Flask
→ SQLAlchemy
→ PostgreSQL
→ Flask
→ React

works end-to-end.

---

## 2. Test Environment

Frontend:

http://localhost:5173

Backend:

http://localhost:5000

API Base:

http://localhost:5000/api/v1

Database:

PostgreSQL

Frontend API Environment:

VITE_API_BASE_URL=http://localhost:5000/api/v1

Backend Frontend Origin:

FRONTEND_ORIGIN=http://localhost:5173

---

## 3. Required Test Accounts

Create four accounts:

### Instructor A

Role:

INSTRUCTOR

### Instructor B

Role:

INSTRUCTOR

### Student A

Role:

STUDENT

### Student B

Role:

STUDENT

Real passwords must not be committed to this document.

---

## 4. Authentication Scenarios

### AUTH-01 — Student Registration

Steps:

1. Open `/register`.
2. Register Student A.
3. Submit valid data.

Expected:

- HTTP 201.
- Account stored in PostgreSQL.
- User receives STUDENT role.
- User can proceed to Login.

Result:

PASS / FAIL

---

### AUTH-02 — Instructor Registration

Steps:

1. Open `/register`.
2. Select Instructor.
3. Submit valid registration data.

Expected:

- HTTP 201.
- Instructor stored.
- Role = INSTRUCTOR.

Result:

PASS / FAIL

---

### AUTH-03 — Duplicate Email

Steps:

1. Register an account.
2. Attempt registration with the same normalized email.

Expected:

HTTP 409.

Expected code:

EMAIL_ALREADY_REGISTERED

No duplicate database User.

Result:

PASS / FAIL

---

### AUTH-04 — Successful Login

Steps:

1. Enter correct email/password.
2. Submit Login.

Expected:

- JWT returned.
- JWT stored by frontend.
- User state restored.
- Student redirects to `/student/dashboard`.
- Instructor redirects to `/instructor/dashboard`.

Result:

PASS / FAIL

---

### AUTH-05 — Incorrect Password

Expected:

HTTP 401.

Code:

INVALID_CREDENTIALS

UI:

Invalid email or password.

Result:

PASS / FAIL

---

### AUTH-06 — Missing JWT

Call protected endpoint without Authorization header.

Expected:

HTTP 401.

Code:

AUTHENTICATION_REQUIRED

Result:

PASS / FAIL

---

### AUTH-07 — Invalid JWT

Send an invalid Bearer token.

Expected:

HTTP 401.

Code:

INVALID_TOKEN

Result:

PASS / FAIL

---

### AUTH-08 — Expired JWT

Use an expired token or configure a short test expiration.

Expected:

- API returns 401.
- Error code = TOKEN_EXPIRED.
- Frontend removes stale token.
- Auth state becomes unauthenticated.
- Protected route returns User to Login.

Result:

PASS / FAIL

---

### AUTH-09 — Browser Refresh

Steps:

1. Login.
2. Open protected Dashboard.
3. Refresh browser.

Expected:

- Stored JWT read.
- `/auth/me` requested.
- User restored.
- Dashboard remains usable.

Result:

PASS / FAIL

---

### AUTH-10 — Logout

Expected:

- Token removed.
- User state cleared.
- Protected routes no longer accessible.

Result:

PASS / FAIL

---

## 5. Instructor Scenarios

### INS-01 — Create Course

Expected:

- Instructor can create Course.
- Course stored as DRAFT.
- Course belongs to current Instructor.

Result:

PASS / FAIL

---

### INS-02 — View Own Courses

Expected:

Instructor Dashboard displays the current Instructor's Courses.

Result:

PASS / FAIL

---

### INS-03 — Edit Own Course

Expected:

- Instructor can update title/description of own Course.
- Database changes persist after refresh.

Result:

PASS / FAIL

---

### INS-04 — Instructor Cannot Edit Another Instructor's Course

Instructor A creates Course.

Instructor B manually attempts update.

Expected:

HTTP 403.

Result:

PASS / FAIL

---

### INS-05 — Create Module

Expected:

- Module stored.
- Module belongs to correct Course.
- UI refreshes.

Result:

PASS / FAIL

---

### INS-06 — Duplicate Module Position

If database/backend enforces unique course position:

Expected:

Conflict/validation error displayed meaningfully.

Result:

PASS / FAIL

---

### INS-07 — Create Lesson

Expected:

- Lesson stored.
- Lesson belongs to correct Module.
- Lesson appears after refresh.

Result:

PASS / FAIL

---

### INS-08 — Publish Course

Expected:

DRAFT → PUBLISHED.

Course appears in public Course Catalog.

Result:

PASS / FAIL

---

### INS-09 — View Enrolled Students

Expected:

Only authorized Instructor/Admin can view Course Students.

Result:

PASS / FAIL

---

### INS-10 — View Student Progress

Expected:

Owning Instructor can view progress of enrolled Student.

Result:

PASS / FAIL

---

## 6. Student Scenarios

### STU-01 — Browse Courses

Expected:

Only published Courses appear in public catalog.

Result:

PASS / FAIL

---

### STU-02 — Course Details

Expected:

Real Course data loaded from backend.

Result:

PASS / FAIL

---

### STU-03 — Enroll

Expected:

- HTTP 201.
- Enrollment stored.
- UI changes from Enroll to Continue Learning.

Result:

PASS / FAIL

---

### STU-04 — Duplicate Enrollment

Submit enrollment twice.

Expected:

HTTP 409.

Code:

ALREADY_ENROLLED

Only one logical Enrollment exists.

Result:

PASS / FAIL

---

### STU-05 — My Courses

Expected:

Student sees only their own enrolled Courses.

Result:

PASS / FAIL

---

### STU-06 — Access Enrolled Lesson

Expected:

Enrolled Student can open Lesson.

Result:

PASS / FAIL

---

### STU-07 — Unenrolled Lesson Access

Student B does not enroll.

Student B manually requests Lesson.

Expected:

HTTP 403.

Code:

COURSE_ENROLLMENT_REQUIRED

Result:

PASS / FAIL

---

### STU-08 — Complete Lesson

Expected:

- LessonProgress created/updated.
- completed = true.
- UI indicates completion.

Result:

PASS / FAIL

---

### STU-09 — Repeat Lesson Completion

Complete same Lesson again.

Expected:

No duplicate logical progress record.

Result:

PASS / FAIL

---

### STU-10 — Course Progress

Expected:

completed_lessons / total_lessons is correctly calculated by backend.

Result:

PASS / FAIL

---

## 7. Quiz Scenarios

### QUIZ-01 — Instructor Creates Quiz

Expected:

Quiz, Questions and Options persist.

Result:

PASS / FAIL

---

### QUIZ-02 — Student Discovers Course Quiz

Expected:

`GET /courses/{course_id}/quizzes`

returns authorized Course quizzes.

Result:

PASS / FAIL

---

### QUIZ-03 — Student Retrieves Quiz

Expected:

Questions/options returned.

Correct-answer flags are not returned.

Result:

PASS / FAIL

---

### QUIZ-04 — Submit Quiz

Expected:

- Backend validates answers.
- Backend calculates score.
- QuizAttempt stored.
- StudentAnswer records stored.
- Score returned.

Result:

PASS / FAIL

---

### QUIZ-05 — Client Cannot Control Score

Attempt to send arbitrary score from frontend/API client.

Expected:

Backend ignores client score and calculates result itself.

Result:

PASS / FAIL

---

### QUIZ-06 — Quiz Attempt History

Expected:

Current Student sees their stored attempts.

Result:

PASS / FAIL

---

## 8. Authorization Scenarios

Verify:

- Student cannot create Course.
- Student cannot edit Course.
- Student cannot publish Course.

- Student cannot manage Modules/Lessons.
- Instructor can create Course.
- Instructor can edit own Course.
- Instructor cannot edit another Instructor's Course.
- Unenrolled Student cannot access protected Lesson.
- Instructor can view Students only for authorized Course.
- Admin endpoints remain backend-protected.

---

## 9. Error Handling Scenarios

Test:

- Invalid Course ID.
- Invalid Module ID.
- Invalid Lesson ID.
- Invalid Quiz ID.
- Duplicate Email.
- Duplicate Enrollment.
- Wrong credentials.
- Forbidden action.
- Database/API failure.
- Request timeout.
- Backend unavailable.

UI must display understandable errors.

---

## 10. CORS Test

Open frontend through:

http://localhost:5173

Perform API request.

Expected:

Browser permits request from configured origin.

Test a different unauthorized origin where practical.

Expected:

Origin is not automatically trusted.

---

## 11. Loading State Verification

Verify:

- Login submission.
- Registration submission.
- Course loading.
- Course creation.
- Enrollment.
- Lesson completion.
- Progress retrieval.
- Quiz retrieval.
- Quiz submission.

No operation should remain permanently stuck in loading state.

---

## 12. Empty State Verification

Verify:

- No public Courses.
- No enrolled Courses.
- No Instructor Courses.
- No Students enrolled.
- No Quizzes.
- No Quiz Attempts.

Empty data is not treated as application failure.

---

## 13. Browser Refresh Scenarios

After creating data:

1. Refresh Course screen.
2. Refresh Student Dashboard.
3. Refresh Progress screen.
4. Refresh Instructor Dashboard.

Expected:

Persistent information reloads from backend/database.

---

## 14. Responsive Verification

Verify:

Desktop.

Tablet.

Mobile.

Core functionality should remain usable.

---

## 15. Final Instructor-to-Student Workflow

Instructor:

Login
→ Create Course
→ Add Module
→ Add Lesson
→ Create Quiz
→ Publish

Student:

Login
→ Browse
→ Open Course
→ Enroll
→ My Courses
→ Open Lesson
→ Complete Lesson
→ View Progress
→ Open Quiz
→ Submit
→ View Result

Expected:

Every step uses the real Flask/PostgreSQL backend.

---

## 16. Final Result

Environment: PASS / FAIL

CORS: PASS / FAIL

Authentication: PASS / FAIL

Authorization: PASS / FAIL

Instructor Workflow: PASS / FAIL

Student Workflow: PASS / FAIL

Quiz Workflow: PASS / FAIL

Error Handling: PASS / FAIL

Persistence: PASS / FAIL

Overall Phase 5:

PASS / FAIL
