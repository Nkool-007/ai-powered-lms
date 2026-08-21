# AI-Powered LMS — Feature Catalogue

## 1. Authentication & Authorization

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| User Registration | Create a new account | Student/Instructor | MUST | Yes |
| Login | Authenticate existing users | All | MUST | Yes |
| Logout | End authenticated session | All | MUST | Yes |
| Secure Password Handling | Passwords must not be stored as readable text | All | MUST | Yes |
| Student Role | Student-specific permissions | Student | MUST | Yes |
| Instructor Role | Instructor-specific permissions | Instructor | MUST | Yes |
| Admin Role | Administrative permissions | Admin | MUST | Yes |
| Protected Functionality | Restrict features to authenticated users | All | MUST | Yes |
| Role-Based Permissions | Restrict actions according to user role | All | MUST | Yes |
| Forgot Password | Account recovery workflow | All | SHOULD | No |
| Social Login | Login using third-party provider | All | COULD | No |

## 2. Course Management

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Create Course | Instructor creates a course | Instructor | MUST | Yes |
| Edit Course | Instructor modifies own course | Instructor | MUST | Yes |
| Delete Course | Instructor removes own course where permitted | Instructor | SHOULD | Yes |
| Course Title | Name of course | Instructor | MUST | Yes |
| Course Description | Overview of learning content | Instructor | MUST | Yes |
| Course Instructor | Associate course with creator | Instructor | MUST | Yes |
| Draft Status | Course can remain unpublished during development | Instructor | MUST | Yes |
| Publish Course | Make course available to students | Instructor | MUST | Yes |
| Unpublish Course | Remove course from public availability | Instructor/Admin | SHOULD | Yes |
| Course Catalogue | Display available published courses | Student | MUST | Yes |
| Course Search | Search catalogue | Student | SHOULD | No |
| Course Category | Categorize courses | Instructor | SHOULD | No |
| Course Rating | Students rate courses | Student | COULD | No |

## 3. Module & Lesson Management

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Create Module | Divide course into sections | Instructor | MUST | Yes |
| Edit Module | Modify module details | Instructor | MUST | Yes |
| Delete Module | Remove unnecessary module | Instructor | MUST | Yes |
| Module Ordering | Define module sequence | Instructor | MUST | Yes |
| Create Lesson | Add learning content | Instructor | MUST | Yes |
| Edit Lesson | Modify learning content | Instructor | MUST | Yes |
| Delete Lesson | Remove lesson | Instructor | MUST | Yes |
| Lesson Ordering | Define lesson sequence | Instructor | MUST | Yes |
| Lesson Viewer | Student reads/views lesson | Student | MUST | Yes |
| Rich Media Lessons | Advanced media support | Student/Instructor | SHOULD | No |

## 4. Course Enrollment

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Enroll in Course | Student joins published course | Student | MUST | Yes |
| Prevent Duplicate Enrollment | Same student cannot enroll twice | Student/System | MUST | Yes |
| My Courses | Show student's enrollments | Student | MUST | Yes |
| View Enrolled Students | Instructor views learners in own course | Instructor | MUST | Yes |
| Unenroll | Student leaves course | Student | COULD | No |
| Enrollment Approval | Instructor manually approves students | Instructor | COULD | No |

## 5. Learning & Content Delivery

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Course Learning Page | Main page for enrolled course | Student | MUST | Yes |
| Module List | Show course modules | Student | MUST | Yes |
| Lesson List | Show lessons under modules | Student | MUST | Yes |
| Lesson Access | Open permitted lesson | Student | MUST | Yes |
| Complete Lesson | Record lesson completion | Student | MUST | Yes |
| Continue Learning | Return quickly to incomplete course | Student | SHOULD | No |
| Downloadable Resources | Additional lesson resources | Student | SHOULD | No |

## 6. Quiz & Assessment

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Create Quiz | Instructor creates an assessment | Instructor | MUST | Yes |
| Create Question | Instructor adds quiz question | Instructor | MUST | Yes |
| Multiple-Choice Options | Provide possible answers | Instructor | MUST | Yes |
| Correct Answer | Store valid answer | Instructor | MUST | Yes |
| Attempt Quiz | Student answers assessment | Student | MUST | Yes |
| Submit Quiz | Submit attempt for evaluation | Student | MUST | Yes |
| Score Calculation | Calculate result | System | MUST | Yes |
| Store Quiz Attempt | Preserve assessment history | System | MUST | Yes |
| View Result | Student sees score | Student | MUST | Yes |
| Instructor Performance View | Instructor sees student results | Instructor | SHOULD | No |
| Question Explanation | Explain correct answer | Student | SHOULD | No |

## 7. Progress Tracking

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Lesson Completion | Record completed lessons | Student | MUST | Yes |
| Completed Lesson Count | Count completed lessons | Student | MUST | Yes |
| Total Lesson Count | Count course lessons | Student | MUST | Yes |
| Completion Percentage | Calculate overall progress | Student | MUST | Yes |
| Student Progress View | Student sees own progress | Student | MUST | Yes |
| Instructor Progress View | Instructor sees learner progress | Instructor | MUST | Yes |
| Advanced Analytics | Detailed engagement analytics | Instructor/Admin | COULD | No |

## 8. AI Features

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| AI Tutor | Ask questions while learning | Student | MUST | Yes |
| Explain Course Concepts | AI explains concepts | Student | MUST | Yes |
| Simplify Explanation | AI provides simpler explanation | Student | MUST | Yes |
| Course-Relevant AI Responses | Keep answers connected to selected course | Student | MUST | Yes |
| AI Quiz Generator | Generate draft quiz questions | Instructor | SHOULD | No |
| Human Review of AI Questions | Instructor approves AI content | Instructor | SHOULD | No |
| Weak Area Identification | Analyze areas needing improvement | Student | COULD | No |
| Personalized Next-Step Recommendation | Suggest next learning activity | Student | COULD | No |
| AI Citations/References | Show source lesson used by AI | Student | COULD | No |
| Streaming AI Responses | Display AI output progressively | Student | COULD | No |
| Multi-Agent Learning System | Multiple specialized AI agents | Student | OUT OF SCOPE | No |

## 9. Admin Features

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Admin Login | Secure administrative access | Admin | MUST | Yes |
| View Users | List platform users | Admin | MUST | Yes |
| View Courses | List platform courses | Admin | MUST | Yes |
| Disable User | Restrict problematic account | Admin | SHOULD | No |
| Reactivate User | Restore user account | Admin | SHOULD | No |
| Moderate Course | Unpublish/remove invalid course | Admin | SHOULD | No |
| Basic Platform Statistics | User/course/enrollment totals | Admin | SHOULD | No |
| Complex Analytics Dashboard | Advanced business analytics | Admin | COULD | No |

## 10. Integration Features

| Feature | Description | Persona | Priority | MVP |
|---|---|---|---|---|
| Email Notifications | Send selected system emails | All | SHOULD | No |
| Password Reset Email | Account recovery | All | SHOULD | No |
| Google Login | Third-party authentication | All | COULD | No |
| Real-Time Notifications | Live platform alerts | All | COULD | No |
| Payment Gateway | Paid course marketplace | Student | OUT OF SCOPE | No |
| Live Video Integration | Built-in live classes | All | OUT OF SCOPE | No |

## 11. DevOps / Production Requirements

These are not end-user product features, but they are mandatory final capstone requirements.

| Requirement | Description | Priority | Final Project Requirement |
|---|---|---|---|
| Version Control | Maintain project repository | MUST | Yes |
| Database Migrations | Manage database changes safely | MUST | Yes |
| Automated Tests | Test important behavior | MUST | Yes |
| Dockerisation | Containerize application | MUST | Yes |
| Docker Compose | Run required services together | SHOULD | Recommended |
| Cloud Deployment | Deploy working application | MUST | Yes |
| Environment Variables | Keep configuration/secrets outside source | MUST | Yes |
| README | Professional project documentation | MUST | Yes |
| API Documentation | Document REST endpoints | SHOULD | Recommended |
| CI/CD | Automate test/build pipeline | SHOULD | Recommended |

## 12. MVP Feature Summary

The Mandatory MVP contains:

1. User registration and login.
2. Student, Instructor and Admin roles.
3. Role-based access.
4. Course creation.
5. Course editing.
6. Modules.
7. Lessons.
8. Course publishing.
9. Course catalogue.
10. Student enrollment.
11. Duplicate enrollment prevention.
12. My Courses.
13. Lesson access.
14. Lesson completion.
15. Quiz creation.
16. Quiz attempt.
17. Automatic scoring.
18. Progress tracking.
19. Instructor progress visibility.
20. Basic administration.
21. Course-aware AI Tutor.
22. AI-assisted explanations.
