# SmartLMS — Phase 8 Production Deployment Test Plan

> The reference expected result is PASS. Students must execute the tests against their own real AWS deployment and record the actual result. Do not write PASS without testing.

| # | Test | Expected Result | Actual Result |
|---:|---|---|---|
| 1 | React Production Build | `npm ci` and `npm run build` complete successfully | TO BE EXECUTED |
| 2 | Frontend Loads Through Public URL | SmartLMS loads from CloudFront | TO BE EXECUTED |
| 3 | CloudFront Serves React | Frontend assets delivered through CloudFront over HTTPS | TO BE EXECUTED |
| 4 | Backend Is Publicly Reachable | Production API responds | TO BE EXECUTED |
| 5 | Backend Health Endpoint | `GET /api/v1/health` returns 200 | TO BE EXECUTED |
| 6 | EC2 Connects to RDS | Flask performs DB operations successfully | TO BE EXECUTED |
| 7 | Production Migrations | `flask db upgrade` completes without schema errors | TO BE EXECUTED |
| 8 | Registration | Valid registration succeeds | TO BE EXECUTED |
| 9 | Login | Valid login returns JWT/user information | TO BE EXECUTED |
| 10 | JWT-Protected API | Authenticated request succeeds; missing/invalid token rejected | TO BE EXECUTED |
| 11 | Instructor Creates Course | Course is stored in RDS | TO BE EXECUTED |
| 12 | Instructor Creates Module & Lesson | Module/Lesson stored correctly | TO BE EXECUTED |
| 13 | Course Publication | Valid Course can be published | TO BE EXECUTED |
| 14 | Student Enrollment | Enrollment succeeds once; duplicate rejected | TO BE EXECUTED |
| 15 | Lesson Completion | LessonProgress stored in RDS | TO BE EXECUTED |
| 16 | Progress Calculation | Progress is calculated correctly | TO BE EXECUTED |
| 17 | Quiz Submission | Backend calculates score and stores QuizAttempt | TO BE EXECUTED |
| 18 | AI Quiz Generator | Valid structured draft returned; no auto-publish | TO BE EXECUTED |
| 19 | Production Course Reindex | `chunks_indexed > 0`; CourseChunk rows stored | TO BE EXECUTED |
| 20 | RAG Tutor | Student receives Course-aware response | TO BE EXECUTED |
| 21 | Tutor Sources | Lesson/Module source metadata returned | TO BE EXECUTED |
| 22 | Cross-Course Retrieval | Course A question retrieves Course A chunks only | TO BE EXECUTED |
| 23 | Production CORS | Production frontend can call backend | TO BE EXECUTED |
| 24 | No Localhost Production Config | Deployed React calls cloud API | TO BE EXECUTED |
| 25 | AI Failure Isolation | AI fails in controlled manner; core LMS still works | TO BE EXECUTED |
| 26 | No Real Secrets Committed | Repository review finds no production secret | TO BE EXECUTED |

## Test Notes

For every failed test record:
- Observed behaviour
- Root cause
- Affected layer
- Fix
- Final behaviour
