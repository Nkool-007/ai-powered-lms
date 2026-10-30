# SmartLMS - Phase 7 Docker Test Plan

## Purpose

Verify that the complete Phase 6 SmartLMS remains operational after Dockerisation.

The reference expected result for every mandatory test is `PASS`. Students must execute each test on their own repository and record the actual observed result.

## Test 1 - Build Frontend Image

**Command**

```bash
docker compose build frontend
```

**Expected:** Frontend image builds without error.  
**Reference Result:** PASS

## Test 2 - Build Backend Image

```bash
docker compose build backend
```

**Expected:** Backend image builds without error.  
**Reference Result:** PASS

## Test 3 - Start PostgreSQL Container

```bash
docker compose up -d postgres
docker compose ps postgres
```

**Expected:** `postgres = healthy`.  
**Reference Result:** PASS

## Test 4 - Backend Connects to PostgreSQL

```bash
docker compose up -d backend
docker compose logs backend
```

**Expected:** No connection-refused or hostname-resolution failure.  
**Reference Result:** PASS

## Test 5 - Database Migrations Run

```bash
docker compose exec backend \
  flask --app run.py db upgrade
```

**Expected:** Migration completes successfully.  
**Reference Result:** PASS

## Test 6 - React Loads

Open:

```text
http://localhost:5173
```

**Expected:** SmartLMS frontend loads.  
**Reference Result:** PASS

## Test 7 - React Calls Flask API

Open the Course Catalog.

**Expected:** Published Course data is obtained from Flask.  
**Reference Result:** PASS

## Test 8 - User Login Works

Login through React.

**Expected:**

```text
POST /auth/login
-> 200
-> JWT received
-> Dashboard displayed
```

**Reference Result:** PASS

## Test 9 - JWT-Protected API Works

Access authenticated Student or Instructor functionality.

**Expected:** JWT is automatically attached through the centralized Axios client.  
**Reference Result:** PASS

## Test 10 - Instructor Course Workflow Works

```text
Instructor Login
-> Create Course
-> Add Module
-> Add Lesson
-> Publish
```

**Expected:** All changes persist in PostgreSQL.  
**Reference Result:** PASS

## Test 11 - Student Enrollment Works

Student enrolls in a published Course.

**Expected:** Enrollment is created once; duplicate enrollment remains rejected.  
**Reference Result:** PASS

## Test 12 - Lesson Completion Works

Student completes a Lesson.

**Expected:** `LessonProgress` is persisted.  
**Reference Result:** PASS

## Test 13 - Quiz Submission Works

Student submits Quiz answers.

**Expected:** Backend calculates score and stores the attempt.  
**Reference Result:** PASS

## Test 14 - Progress Persists

Complete multiple Lessons and restart the browser/application.

**Expected:** Progress still reflects PostgreSQL state.  
**Reference Result:** PASS

## Test 15 - Database Data Survives Container Restart

Create data, then run:

```bash
docker compose down
docker compose up -d
```

**Expected:** Previously created data remains.  
**Reference Result:** PASS

## Test 16 - AI Quiz Generator Works From Containers

```text
Instructor
-> Lesson
-> Generate Quiz With AI
```

**Expected:** Structured Quiz draft is returned.  
**Reference Result:** PASS

## Test 17 - Course Reindexing Works

Call:

```text
POST /api/v1/ai/courses/{course_id}/reindex
```

**Expected:** `chunks_indexed > 0` and `CourseChunk` rows exist.  
**Reference Result:** PASS

## Test 18 - RAG Tutor Works

An enrolled Student asks a Course question.

**Expected:**

```text
Question
-> Embedding
-> pgvector retrieval
-> Course context
-> LLM
-> Answer + Sources
```

**Reference Result:** PASS

## Test 19 - Course Isolation Still Works

Create Course A and Course B with different content, then ask a Course A question.

**Expected:** Every retrieved chunk belongs to Course A; no Course B source appears.  
**Reference Result:** PASS

## Test 20 - AI Failure Does Not Break Core LMS

Simulate unavailable AI credentials/provider.

**Expected:** AI request returns a controlled error while Login, Course Catalog, Lessons, Enrollment, Progress, and Quiz continue working.  
**Reference Result:** PASS

## Additional Recommended Verification

- [ ] `docker compose ps` reports healthy services.
- [ ] `.env` is not tracked.
- [ ] PostgreSQL has no public host port.
- [ ] pgvector extension exists.
- [ ] Migrations can run against a fresh volume.
- [ ] Backend logs are accessible.
- [ ] Frontend logs are accessible.
- [ ] PostgreSQL logs are accessible.
