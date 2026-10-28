# AI-Powered LMS — Project Scope


## 1. Purpose of This Document
This document defines the boundaries of the AI-Powered LMS Capstone Project.

Its purpose is to prevent uncontrolled feature expansion and ensure the team focuses first
on building a small but complete product.

The project is not intended to reproduce every feature available in commercial LMS
platforms.

The priority is:

      Complete core functionality before expanding functionality.


## 2. In Scope — Mandatory MVP
The following functionality is part of the mandatory product scope.

### 2.1 User Management
The product will support three roles:

- Student
- Instructor
- Admin

Mandatory capabilities:

- Registration where applicable.
- Login.
- Logout.
- Secure authentication.
- Role identification.
- Role-based authorization.


### 2.2 Student Capabilities
A Student will be able to:

- Register.
- Login.
- Browse published courses.
- View course details.
- Enroll in courses.
- View enrolled courses.
- Access modules.
- Access lessons.
- Mark lessons as completed.
- Attempt quizzes.
- View quiz scores.
- Track course progress.
- Ask questions to the AI Tutor.


### 2.3 Instructor Capabilities
An Instructor will be able to:

- Login.
- Create a course.
- Edit their own course.
- Create modules.
- Create lessons.
- Organize learning content.
- Create basic quizzes.
- Add multiple-choice questions.
- Publish a course.
- View enrolled students.
- View basic student progress.

An Instructor should not normally be able to edit another instructor's course.


### 2.4 Admin Capabilities
The mandatory Admin scope will remain deliberately small.

The Admin will be able to:

- Login.
- View platform users.
- View platform courses.

More advanced moderation functionality may be added after the core LMS works.


### 2.5 Course Management
The mandatory course model will support:

- Course title.
- Course description.
- Instructor ownership.
- Draft/published state.
- Modules.
- Lessons.
- Ordered learning structure.

The project does not need to reproduce every course-authoring capability available in
commercial LMS products.

### 2.6 Enrollment
Mandatory enrollment functionality includes:

- Student enrollment in published courses.
- Prevention of duplicate enrollment.
- Student view of enrolled courses.
- Instructor view of students enrolled in their courses.


### 2.7 Learning Delivery
The mandatory learning experience includes:

Course → Module → Lesson

Students should be able to:

- Navigate course structure.
- Access relevant lessons.
- Complete lessons.
- Continue progressing through the course.


### 2.8 Quiz & Assessment
The mandatory assessment scope is intentionally limited to a basic quiz system.

It will support:

- Quiz creation.
- Multiple-choice questions.
- Answer options.
- Correct answer.
- Student attempts.
- Quiz submission.
- Score calculation.
- Storing quiz attempts.
- Viewing results.

Advanced examination systems are outside the initial MVP.

### 2.9 Progress Tracking
Mandatory progress functionality includes:

- Recording lesson completion.
- Counting completed lessons.
- Counting total lessons.
- Calculating course completion percentage.
- Showing progress to students.
- Allowing instructors to view basic student progress.

The project does not require complex learning analytics for the MVP.


### 2.10 AI Learning Assistant
At least one meaningful AI capability is mandatory.

The primary AI feature will be:


Course-Aware AI Tutor
Students will be able to ask questions related to the course they are studying.

The AI Tutor should aim to:

- Answer course-related questions.
- Explain concepts.
- Simplify difficult explanations.
- Support learning without replacing instructor-controlled course content.

AI should enhance the LMS rather than exist as a disconnected chatbot.


## 3. In Scope — Optional / Should Have
The following features may be implemented after mandatory functionality is working and
stable.


### 3.1 AI Quiz Generator

Allow instructors to generate draft quiz questions using AI.

Expected flow:

Lesson Material → AI Generates Questions → Instructor Reviews → Instructor
Approves/Edits → Save

AI output should not automatically become approved educational content.


### 3.2 Instructor Assessment View
Allow instructors to view student quiz performance.


### 3.3 Admin User Management
Possible capabilities:

- Disable user.
- Reactivate user.
- Moderate problematic accounts.


### 3.4 Course Moderation
Admin may:

- Unpublish inappropriate course.
- Remove invalid course.


### 3.5 Basic Admin Dashboard
Possible information:

- Total students.
- Total instructors.
- Total courses.
- Total enrollments.

### 3.6 Course Search
Allow students to search available courses.


### 3.7 Email Notifications
Possible examples:

- Registration confirmation.
- Enrollment confirmation.
- Course reminder.
- Password reset.


### 3.8 Question Explanations
After completing a quiz, students may receive explanations for answers.


## 4. Stretch Goals
These features should be attempted only after the complete mandatory project is stable.


### 4.1 Personalized AI Learning Recommendations
AI analyzes:

- Student progress.
- Incomplete lessons.
- Quiz performance.

and recommends what the learner should study next.


### 4.2 Weak Area Identification
AI identifies topics in which a student has repeatedly performed poorly.

Example:

        "Your results suggest that SQL JOIN operations require further revision."


### 4.3 AI Learning Plan
AI may generate a short personalized study plan based on course progress.


### 4.4 AI Answer Citations
AI answers may reference the relevant:

- Course.
- Module.
- Lesson.

Example:

        Source: Module 4 → Lesson 2 — Python Decorators


### 4.5 Streaming AI Responses
AI responses may appear progressively rather than waiting for the entire answer.


### 4.6 Advanced Instructor Analytics
Possible capabilities:

- Average course progress.
- Quiz performance distribution.
- Frequently missed questions.
- Student engagement indicators.


### 4.7 OAuth Login
Possible third-party login such as Google authentication.

### 4.8 Advanced DevOps
Possible enhancements:

- Automated CI/CD.
- Automated deployment.
- Monitoring.
- Application logging.
- Production observability.


## 5. Explicitly Out of Scope
The following features will not be part of the standard Capstone Project scope.


### 5.1 Built-In Live Video Conferencing
The project will not build its own Zoom/Google Meet-style video conferencing system.


### 5.2 Native Mobile Applications
The project will not include separate:

- Android application.
- iOS application.

The initial product will be web-based.


### 5.3 Full Course Marketplace
The project will not attempt to reproduce the complete commercial marketplace functionality
of platforms such as Udemy.

### 5.4 Payment Processing
A full payment marketplace is outside the standard scope.

Examples excluded:

- Purchasing courses.
- Instructor payouts.
- Refund management.
- Tax calculation.
- Subscription billing.


### 5.5 Student Social Network
The project will not contain a full Facebook/LinkedIn-style social network.


### 5.6 Student-to-Student Real-Time Chat
A complete messaging/chat platform is outside the MVP.


### 5.7 Complex Discussion Forums
A Reddit/Stack Overflow-style discussion system is outside the standard project.


### 5.8 Advanced Certificate System
Automated certificates, verification IDs, blockchain credentials, etc. are outside the
mandatory scope.


### 5.9 Attendance Management
Traditional classroom attendance management is outside the standard project.

### 5.10 SCORM Integration
Support for full SCORM content standards is outside the scope.


### 5.11 Complex Recommendation Engine
A production-scale recommendation engine comparable to commercial learning platforms is
outside the MVP.


### 5.12 Multi-Agent AI Architecture
The mandatory product does not require multiple interacting AI agents.

A single meaningful AI learning assistant is sufficient.


### 5.13 AI Replacing the Instructor
The AI system will not autonomously control:

- Course publishing.
- Official educational content.
- Final assessment decisions.
- Instructor authority.

AI is an assistant, not the owner of educational content.


## 6. MVP Boundary
The MVP can be summarized as:

        A student should be able to create an account, login, discover a published
        course, enroll, study structured lessons, attempt a quiz, track progress,
        and ask an AI Tutor for help.

At the same time:

        An instructor should be able to create, organize and publish that course
        and monitor basic student progress.

And:

        An Admin should have basic visibility into the users and courses on the
        platform.

If these journeys work correctly, the core product exists.

Everything else is secondary.


## 7. MVP User Journey
Instructor Journey
Login

↓

Create Course

↓

Add Modules

↓

Add Lessons

↓

Create Quiz

↓

Publish Course

↓

View Students and Progress


Student Journey
Register

↓

Login

↓

Browse Course

↓

View Details

↓

Enroll

↓

Study Lessons

↓

Complete Lessons

↓

Attempt Quiz

↓

View Score

↓

Track Progress

↓

Ask AI Tutor


Admin Journey
Login

↓

View Users

↓

View Courses

↓

Perform Basic Administration


## 8. AI Scope Boundary
The MVP AI system is intended to solve:

         "I am studying this course and I do not understand something. Can the
         system help me?"

The MVP AI system is not intended to solve every educational problem.

Mandatory

- Course-related Q&A.
- Concept explanation.
- Simplification of difficult topics.

Optional

- AI quiz generation.

Stretch

- Weak-area identification.
- Personalized recommendations.
- Next-lesson recommendations.
- AI citations.
- AI-generated learning plans.

Out of Scope

- Fully autonomous AI instructor.
- Complex multi-agent educational ecosystem.
- Automatic unsupervised course publishing.


## 9. Scope Control Rules
The following rules should guide project development.

Rule 1

Mandatory features are completed before optional features.

Rule 2

Optional features are completed before stretch features.

Rule 3

A new feature should not be added simply because another LMS contains it.

Rule 4

Any feature that significantly increases complexity must be justified.

Rule 5

AI must provide meaningful educational value.

Rule 6

The core LMS should continue to function even if AI functionality temporarily fails.

Rule 7

A complete smaller product is preferred over an incomplete larger product.


## 10. Final Scope Classification
MUST HAVE
- Authentication.
- Student role.
- Instructor role.
- Admin role.
- Authorization.
- Course creation.
- Modules.
- Lessons.
- Publishing.
- Course catalogue.
- Enrollment.
- Duplicate enrollment prevention.

- Learning content access.
- Lesson completion.
- Quiz creation.
- Quiz attempts.
- Scoring.
- Progress tracking.
- AI Tutor.
- Basic Admin visibility.


SHOULD HAVE
- AI Quiz Generator.
- Instructor quiz-performance view.
- Admin moderation.
- Course search.
- Email notifications.
- Better quiz feedback.
- Basic Admin dashboard.


COULD HAVE / STRETCH
- Personalized AI recommendations.
- Weak-area analysis.
- AI study plan.
- AI citations.
- Streaming AI.
- OAuth.
- Advanced analytics.
- Advanced observability.


OUT OF SCOPE
- Native mobile apps.
- Built-in video conferencing.
- Full payment marketplace.
- Student social network.
- Real-time student chat.
- Advanced certificate system.
- Attendance.
- SCORM.

- Production-scale recommendation system.
- Mandatory multi-agent architecture.
- AI autonomously replacing instructors.


## 11. Definition of Product Scope Success
Phase 1 scope definition is successful when every team member can clearly answer:

Who uses the platform?

Student, Instructor, and Admin.

What is the central product?

A structured LMS enhanced with AI-assisted learning.

What is the mandatory AI feature?

A course-aware AI Learning Assistant.

What is the student's central journey?

Discover → Enroll → Learn → Assess → Track → Ask AI

What is the instructor's central journey?

Create → Structure → Assess → Publish → Monitor

What is not being built?

A large collection of unrelated features such as a video conferencing system, mobile
applications, payment marketplace, social network, and complex multi-agent architecture.
