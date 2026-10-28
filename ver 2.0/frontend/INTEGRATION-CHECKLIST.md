# SmartLMS Frontend Integration Checklist

Use this checklist with the Phase 5 backend.

## Environment

- [ ] Flask runs on `http://localhost:5000`
- [ ] React runs on `http://localhost:5173`
- [ ] `VITE_API_BASE_URL=http://localhost:5000/api/v1`
- [ ] Backend allows `FRONTEND_ORIGIN=http://localhost:5173`

## Authentication

- [ ] Student registration works
- [ ] Instructor registration works
- [ ] Duplicate email displays backend message
- [ ] Login stores JWT
- [ ] Student redirects to `/student/dashboard`
- [ ] Instructor redirects to `/instructor/dashboard`
- [ ] Browser refresh restores User via `/auth/me`
- [ ] Logout clears session
- [ ] Expired JWT clears stale session
- [ ] 403 does not automatically log out User

## Instructor

- [ ] Create Course
- [ ] View own Courses
- [ ] Edit own Course
- [ ] Add Module
- [ ] Add Lesson
- [ ] Create Quiz
- [ ] Publish Course
- [ ] View enrolled Students
- [ ] View Student progress
- [ ] Instructor B cannot edit Instructor A's Course

## Student

- [ ] Browse published Courses
- [ ] Open Course details
- [ ] Enroll
- [ ] Duplicate enrollment handled
- [ ] My Courses persists after refresh
- [ ] Enrolled Lesson opens
- [ ] Unenrolled Lesson is rejected
- [ ] Mark Lesson complete
- [ ] Progress updates
- [ ] Course Quizzes are discovered
- [ ] Quiz does not reveal correct answers
- [ ] Quiz submission displays backend score
- [ ] Attempt history persists

## Failure States

- [ ] Backend unavailable
- [ ] Request timeout
- [ ] Invalid Course ID
- [ ] Invalid Lesson ID
- [ ] Invalid Quiz ID
- [ ] Wrong credentials
- [ ] Forbidden action
- [ ] Duplicate enrollment
- [ ] Course publishing validation failure
- [ ] Empty Course catalog
- [ ] Empty My Courses
- [ ] Empty Instructor Courses
- [ ] Empty enrolled Students
- [ ] Empty Quiz list
- [ ] Empty Quiz attempts
