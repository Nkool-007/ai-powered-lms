# AI-Powered LMS — User Stories

## 1. Priority Definitions

### MUST HAVE
Required for the core product to be considered complete.

### SHOULD HAVE
Important and valuable, but the MVP can operate without it.

### COULD HAVE
Useful enhancement if sufficient time remains.

### OUT OF SCOPE
Deliberately excluded from this capstone.

## 2. Student User Stories

### STU-01 — Registration
**Persona:** Student  
**User Story:** As a visitor, I want to register for the platform so that I can create a student account.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- The visitor can provide the required registration information.
- Duplicate account identifiers such as the same email should not create multiple accounts.
- A successfully created user receives a Student role unless another approved registration process applies.

### STU-02 — Login
**Persona:** Student  
**User Story:** As a student, I want to login so that I can securely access my learning account.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Valid credentials allow login.
- Invalid credentials are rejected.
- Successful login gives access to student functionality.

### STU-03 — Browse Courses
**Persona:** Student  
**User Story:** As a student, I want to browse available published courses so that I can discover learning opportunities.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Published courses are visible.
- Unpublished/draft courses are not displayed in the normal catalogue.

### STU-04 — View Course Details
**Persona:** Student  
**User Story:** As a student, I want to view course details before enrolling so that I can decide whether the course is relevant to me.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
The student can view essential information including:
- Course title.
- Description.
- Instructor.
- Basic course structure where appropriate.
- Enrollment status.

### STU-05 — Enroll in Course
**Persona:** Student  
**User Story:** As a student, I want to enroll in a published course so that I can access its learning material.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- An authenticated student can enroll.
- Only valid published courses can be enrolled in.
- Duplicate enrollment is prevented.

### STU-06 — View My Courses
**Persona:** Student  
**User Story:** As a student, I want to see all courses in which I am enrolled so that I can continue my learning.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- The student sees their enrolled courses.
- Courses belonging to other students do not appear as personal enrollments.

### STU-07 — View Course Structure
**Persona:** Student  
**User Story:** As a student, I want to view modules and lessons in a logical order so that I can follow the course structure.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Modules appear in their intended order.
- Lessons appear under the correct module.

### STU-08 — Access Lesson
**Persona:** Student  
**User Story:** As a student, I want to open lessons from my enrolled course so that I can study the learning material.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- An enrolled student can access eligible lesson content.
- Unauthorized access should be rejected where enrollment is required.

### STU-09 — Complete Lesson
**Persona:** Student  
**User Story:** As a student, I want to mark a lesson as completed so that my learning progress can be recorded.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Lesson completion is recorded for the current student.
- Completing one student's lesson does not alter another student's progress.

### STU-10 — Attempt Quiz
**Persona:** Student  
**User Story:** As a student, I want to attempt a course quiz so that I can test my understanding.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Student can answer available questions.
- Student can submit an attempt.
- Submission is stored.

### STU-11 — View Quiz Result
**Persona:** Student  
**User Story:** As a student, I want to view my quiz result so that I can understand how well I performed.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- A submitted quiz receives a score.
- The score is associated with the correct student and attempt.

### STU-12 — Track Course Progress
**Persona:** Student  
**User Story:** As a student, I want to see my course completion progress so that I know how much learning remains.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
The student can see information such as:
- Completed lessons.
- Total lessons.
- Completion percentage.

### STU-13 — Continue Learning
**Persona:** Student  
**User Story:** As a student, I want to quickly return to my incomplete course so that I can continue learning.  
**Priority:** SHOULD HAVE  

**Acceptance Expectation:**  
The student dashboard makes enrolled and incomplete courses easy to access.

### STU-14 — Email Learning Reminder
**Persona:** Student  
**User Story:** As a student, I want to receive optional course reminders so that I do not forget about my learning.  
**Priority:** SHOULD HAVE  

**Acceptance Expectation:**  
Implemented only after the mandatory LMS is stable.

### STU-15 — Course Completion Certificate
**Persona:** Student  
**User Story:** As a student, I want to receive a course certificate after completion so that I have evidence of completion.  
**Priority:** COULD HAVE  

**Acceptance Expectation:**  
Not part of the mandatory MVP.

## 3. Instructor User Stories

### INS-01 — Instructor Login
**Persona:** Instructor  
**User Story:** As an instructor, I want to login so that I can access my course management dashboard.  
**Priority:** MUST HAVE

### INS-02 — Create Course
**Persona:** Instructor  
**User Story:** As an instructor, I want to create a course so that I can provide structured learning material to students.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Instructor can create a new course.
- The course initially belongs to the instructor who created it.

### INS-03 — Edit Own Course
**Persona:** Instructor  
**User Story:** As an instructor, I want to edit my own courses so that I can keep their information and learning material updated.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Instructor can edit courses owned by them.
- One instructor cannot edit another instructor's course without elevated permission.

### INS-04 — Create Modules
**Persona:** Instructor  
**User Story:** As an instructor, I want to divide a course into modules so that learning content is organized into meaningful sections.  
**Priority:** MUST HAVE

### INS-05 — Create Lessons
**Persona:** Instructor  
**User Story:** As an instructor, I want to add lessons to modules so that students can study individual topics.  
**Priority:** MUST HAVE

### INS-06 — Organize Content
**Persona:** Instructor  
**User Story:** As an instructor, I want lessons to have a defined order so that students can follow the intended learning sequence.  
**Priority:** MUST HAVE

### INS-07 — Publish Course
**Persona:** Instructor  
**User Story:** As an instructor, I want to publish a completed course so that students can discover and enroll in it.  
**Priority:** MUST HAVE  

**Acceptance Expectation:**
- Draft courses remain hidden from normal student discovery.
- Published courses become available to students.

### INS-08 — Create Quiz
**Persona:** Instructor  
**User Story:** As an instructor, I want to create quizzes so that I can assess student learning.  
**Priority:** MUST HAVE

### INS-09 — View Enrolled Students
**Persona:** Instructor  
**User Story:** As an instructor, I want to view students enrolled in my course so that I know who is learning from it.  
**Priority:** MUST HAVE

### INS-10 — View Student Progress
**Persona:** Instructor  
**User Story:** As an instructor, I want to view student progress so that I can understand engagement with my course.  
**Priority:** MUST HAVE

### INS-11 — View Assessment Performance
**Persona:** Instructor  
**User Story:** As an instructor, I want to view quiz performance so that I can understand how students are performing.  
**Priority:** SHOULD HAVE

### INS-12 — Generate Quiz With AI
**Persona:** Instructor  
**User Story:** As an instructor, I want AI to generate draft quiz questions from learning material so that I can reduce repetitive assessment creation work.  
**Priority:** SHOULD HAVE  

**Acceptance Expectation:**  
AI output is presented as a draft and is not automatically treated as approved course content.

### INS-13 — Review AI-Generated Questions
**Persona:** Instructor  
**User Story:** As an instructor, I want to review and modify AI-generated questions before saving them so that I remain responsible for educational quality.  
**Priority:** SHOULD HAVE

## 4. Admin User Stories

### ADM-01 — Admin Login
**Persona:** Admin  
**User Story:** As an Admin, I want to login securely so that I can access platform administration functionality.  
**Priority:** MUST HAVE

### ADM-02 — View Users
**Persona:** Admin  
**User Story:** As an Admin, I want to view registered users so that I can manage platform accounts.  
**Priority:** MUST HAVE

### ADM-03 — Manage User Status
**Persona:** Admin  
**User Story:** As an Admin, I want to disable or reactivate users so that inappropriate accounts can be controlled.  
**Priority:** SHOULD HAVE

### ADM-04 — View Courses
**Persona:** Admin  
**User Story:** As an Admin, I want to view courses on the platform so that I can oversee published learning content.  
**Priority:** MUST HAVE

### ADM-05 — Moderate Courses
**Persona:** Admin  
**User Story:** As an Admin, I want to unpublish or remove inappropriate courses so that the platform can be moderated.  
**Priority:** SHOULD HAVE

### ADM-06 — View Platform Statistics
**Persona:** Admin  
**User Story:** As an Admin, I want to view basic platform statistics so that I can understand overall system usage.  
**Priority:** SHOULD HAVE  

**Possible Statistics:**
- Total users.
- Total students.
- Total instructors.
- Total courses.
- Total enrollments.

## 5. AI / Overall-System User Stories

### AI-01 — Ask Course Question
**Persona:** Student  
**User Story:** As a student, I want to ask the AI Tutor questions about my course so that I can receive help when I do not understand a topic.  
**Priority:** MUST HAVE

### AI-02 — Simplify Explanation
**Persona:** Student  
**User Story:** As a student, I want the AI Tutor to explain difficult course concepts in simpler language so that I can understand them more easily.  
**Priority:** MUST HAVE

### AI-03 — Course-Relevant Assistance
**Persona:** Student  
**User Story:** As a student, I want AI responses to remain relevant to the course I am studying so that unrelated information does not interfere with my learning.  
**Priority:** MUST HAVE

### AI-04 — Generate Quiz Questions
**Persona:** Instructor  
**User Story:** As an instructor, I want AI to generate draft quiz questions so that I can create assessments more efficiently.  
**Priority:** SHOULD HAVE

### AI-05 — Human Review of AI Content
**Persona:** Instructor  
**User Story:** As an instructor, I want to review AI-generated educational content before it becomes part of my course so that incorrect output is not automatically published.  
**Priority:** SHOULD HAVE

### AI-06 — Recommend Next Learning Activity
**Persona:** Student  
**User Story:** As a student, I want the AI assistant to recommend what I should study next based on my learning progress so that I can focus on useful learning activities.  
**Priority:** COULD HAVE

### AI-07 — Identify Weak Areas
**Persona:** Student  
**User Story:** As a student, I want AI to identify topics in which I performed poorly so that I know what to revise.  
**Priority:** COULD HAVE

### SYS-01 — Role-Based Access
**Persona:** All Users  
**User Story:** As a platform user, I want functionality to be restricted according to my role so that users cannot perform actions they are not authorized to perform.  
**Priority:** MUST HAVE

### SYS-02 — AI Failure Independence
**Persona:** All Users  
**User Story:** As a user, I want core LMS functionality to remain available even if the AI service is temporarily unavailable so that learning does not completely stop.  
**Priority:** SHOULD HAVE

## 6. Explicitly Out-of-Scope User Stories

### OOS-01
As a student, I want to attend built-in live video classes.  
**Priority:** OUT OF SCOPE

### OOS-02
As a student, I want a native Android/iOS LMS application.  
**Priority:** OUT OF SCOPE

### OOS-03
As a student, I want a complete social networking feed inside the LMS.  
**Priority:** OUT OF SCOPE

### OOS-04
As a student, I want to make marketplace payments for courses.  
**Priority:** OUT OF SCOPE

### OOS-05
As a student, I want to directly chat with every other learner on the platform.  
**Priority:** OUT OF SCOPE
