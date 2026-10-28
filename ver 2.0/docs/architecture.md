# AI-Powered LMS — System Architecture
## 1. Architecture Overview
The AI-Powered Learning Management System uses a client-server architecture.

The application consists of five major logical components:

## 1. React Frontend
## 2. Flask REST API
## 3. PostgreSQL Database
## 4. AI Service
## 5. Vector Store

The React application provides the user interface but does not communicate directly with the
database.

All business operations pass through the Flask REST API.

The backend is responsible for:

- Authentication
- Authorization
- Business rules
- Input validation
- Database operations
- AI integration
- Error handling

PostgreSQL stores structured LMS data such as users, courses, lessons, enrollments,
quizzes, progress, and AI conversations.

The AI Service allows students to interact with a Course-Aware AI Tutor. The backend
controls what information can be sent to the AI service.

A Vector Store may later be used by the AI Tutor to retrieve relevant course material using
embeddings.

The core architecture is intentionally kept as a modular monolithic application rather than
unnecessarily splitting the project into many microservices.


## 2. High-Level Architecture
               USERS
        Student / Instructor / Admin
                  │
                  │
                HTTPS
                  │
                  ▼
           ┌──────────────────┐
           │ React Frontend │
           │            │
           │ User Interface │
           └────────┬─────────┘
                 │
                 │ REST / HTTPS
                 │ JSON
                 ▼
           ┌──────────────────┐
           │ Flask REST API │
           │            │
           │ Authentication │

          │ Authorization │
          │ Business Logic │
          │ Validation    │
          └─────┬──────┬─────┘
             │     │
             │     │
        SQLAlchemy│      │AI API Calls
             │     │
             ▼      ▼
        ┌────────────┐ ┌───────────────┐
        │ PostgreSQL │ │ AI Service │
        │        │ │          │
        │ LMS Data │ │ LLM Provider │
        └────────────┘ └───────┬───────┘
                       │
                       │ Retrieval
                       ▼
                  ┌───────────────┐
                  │ Vector Store │
                  │         │
                  │ Course Chunks │
                  │ + Embeddings │
                  └───────────────┘


## 3. Major Design Decision
The architecture follows this rule:

      The frontend requests actions. The backend decides whether those
      actions are allowed.

For example, hiding the Create Course button from a Student in React is useful for user
experience, but it is not sufficient security.

A Student could manually send:

POST /api/v1/courses

Therefore, Flask must independently verify:

Is the user authenticated?

↓

What role does the user have?

↓

Is that role allowed to create courses?

↓

If no → 403 Forbidden

The backend is therefore the authoritative application layer.


## 4. Component Responsibilities
### 4.1 React Frontend
The React application is responsible for presentation and user interaction.

Responsibilities include:

- Displaying pages.
- Displaying navigation.
- Collecting form input.
- Sending HTTP requests.
- Displaying API responses.
- Maintaining frontend authentication state.
- Providing public and protected routes.
- Displaying courses.
- Displaying lessons.
- Displaying progress.
- Displaying quizzes.
- Displaying AI conversations.
- Handling loading states.
- Displaying errors.

React is not responsible for enforcing actual security.


### 4.2 Flask REST API
The Flask REST API is the central application layer.

Responsibilities include:

**Authentication**

- Registration.
- Login.
- Password verification.
- JWT generation.
- JWT validation.

Authorization

- Student permissions.
- Instructor permissions.
- Admin permissions.
- Ownership checks.

LMS Business Logic

- Course creation.
- Course publishing.
- Enrollment.
- Lesson access.
- Progress updates.
- Quiz scoring.
- Student results.

Database Access

The backend communicates with PostgreSQL through:

Flask
  ↓
SQLAlchemy
  ↓
PostgreSQL

AI Integration

The backend:

- Checks user access.
- Determines the current course.
- Retrieves relevant course context.
- Sends controlled context to the AI service.
- Receives the AI response.
- Stores conversation history where appropriate.
- Returns the answer to React.

### 4.3 PostgreSQL
PostgreSQL stores structured application data.

Examples:

Users
Courses
Modules
Lessons
Enrollments
Lesson Progress
Quizzes
Questions
Answer Options
Quiz Attempts
Student Answers
AI Conversations
AI Messages

PostgreSQL is appropriate because the LMS contains many strongly related entities and
requires:

- Primary keys.
- Foreign keys.
- Unique constraints.
- Transactions.
- Referential integrity.
- Relational queries.


### 4.4 AI Service
The AI Service represents communication with an external Large Language Model.

Possible providers may include:

- OpenAI
- Gemini
- another approved LLM provider

The AI provider does not directly access PostgreSQL.

Instead:

LLM

↑
Controlled Context
↑
Flask Backend
↑
Database / Retrieval

This keeps authentication, authorization, and application data under backend control.


### 4.5 Vector Store
The Vector Store is a logical component used by the future RAG-based AI Tutor.

A future ingestion pipeline may work as:

Published Lesson
    ↓
Extract Text
    ↓
Clean Text
    ↓
Split Into Chunks
    ↓
Create Embeddings
    ↓
Store Vectors + Metadata

Each chunk should retain metadata such as:

course_id
module_id
lesson_id
chunk_id

When a Student asks a question:

Question
  ↓
Create Query Embedding
  ↓
Similarity Search
  ↓
Filter by course_id
  ↓
Relevant Course Chunks

 ↓
LLM
 ↓
Answer

For this reference design, the vector store is treated as a logical service.

A later implementation may use PostgreSQL with pgvector or another suitable vector
database.


## 5. Communication Between Components
Browser → React
The user interacts with the React UI.


React → Flask
Protocol:

HTTPS
REST
JSON

Example:

POST /api/v1/courses/12/enroll
Authorization: Bearer <JWT>


Flask → PostgreSQL
Communication occurs through SQLAlchemy.

Conceptually:

REST Request
   ↓
Flask Route
   ↓
Business Logic

  ↓
SQLAlchemy
  ↓
PostgreSQL


Flask → AI Provider
Communication occurs through the provider's API.

Conceptually:

Flask
 ↓
HTTPS API Request
 ↓
LLM Provider
 ↓
AI Response


## 6. Authentication Architecture
The system uses JWT-based authentication.


Login Flow
Student
  │
  ▼
React Login Form
  │
  ▼
POST /api/v1/auth/login
  │
  ▼
Flask
  │
  ├── Find User
  ├── Verify Password Hash
  └── Verify Account Is Active
  │
  ▼
Generate JWT
  │
  ▼

Return Token + User Information
 │
 ▼
React Stores Authentication State
 │
 ▼
JWT Sent With Protected Requests

Example:

Authorization: Bearer eyJ...


## 7. Password Handling
Passwords must never be stored as plaintext.

Incorrect:

password = "mypassword123"

Database should contain:

password_hash

Password verification occurs in the backend.


## 8. JWT Responsibilities
The token identifies the authenticated user.

The backend can derive information such as:

user_id
role
token expiry

A JWT should have an expiration period.

For the MVP, logout can be implemented by deleting the client-side token.

Server-side token revocation can be added later if required.

## 9. Authorization Model
Three roles exist:

STUDENT
INSTRUCTOR
ADMIN

Authentication determines:

      Who are you?

Authorization determines:

      What are you allowed to do?


## 10. Role Permission Matrix
             Action                    Student    Instructor   Admin

 Browse published courses        Yes             Yes           Yes

 View published course details   Yes             Yes           Yes

 Enroll in course                Yes             No            No

 View own enrolled courses       Yes             No            No

 Access enrolled lesson          Yes             No            Yes

 Complete lesson                 Yes             No            No

 Attempt quiz                    Yes             No            No

 View own quiz results           Yes             No            Yes

 Create course                   No              Yes           No

 Edit own course                 No              Yes           No

 Edit another instructor's       No              No            No
 course

 Publish own course              No              Yes           No

 Create module                   No              Course        No
                                                 Owner

 Create lesson                   No                 Course          No
                                                    Owner

 Create quiz                     No                 Course          No
                                                    Owner

 View enrolled students          No                 Own Courses     Yes

 View student progress           No                 Own Courses     Yes

 Ask AI Tutor                    Enrolled Student No                No

 View platform users             No                 No              Yes

 View platform courses           No                 No              Yes

For this reference solution, Admin manages the platform but does not act as a course
author.


## 11. Course Creation Data Flow
Instructor
   │
   ▼
React Create Course Form
   │
   ▼
POST /api/v1/courses
   │
   ▼
JWT Validation
   │
   ▼
Role Check
INSTRUCTOR?
   │
   ▼
Validate Request
   │
   ▼
Create Course
status = DRAFT
   │
   ▼
PostgreSQL
   │

  ▼
201 Created
  │
  ▼
React Displays Course


## 12. Enrollment Data Flow
Student
  │
  ▼
Enroll Button
  │
  ▼
POST /courses/{id}/enroll
  │
  ▼
Authenticate Student
  │
  ▼
Check Course Exists
  │
  ▼
Check Course Is Published
  │
  ▼
Check Existing Enrollment
  │
  ├── Already Enrolled → 409
  │
  ▼
Create Enrollment
  │
  ▼
PostgreSQL
  │
  ▼
201 Created

Duplicate enrollment is protected by:

## 1. Application logic.
## 2. Database unique constraint.

## 13. Student Learning Flow
Login
 ↓
Browse Published Courses
 ↓
View Course
 ↓
Enroll
 ↓
My Courses
 ↓
Open Course
 ↓
View Modules
 ↓
Open Lesson
 ↓
Mark Lesson Complete
 ↓
Progress Updated
 ↓
Attempt Quiz
 ↓
View Result


## 14. Progress Flow
Student completes Lesson 7
    ↓
POST /lessons/7/complete
    ↓
Check Student Enrollment
    ↓
Create / Update LessonProgress
    ↓
Count Completed Lessons
    ↓
Count Course Lessons
    ↓
Calculate Percentage
    ↓
Return Progress

Formula:

Progress Percentage =
Completed Lessons
- ---------------- × 100
Total Lessons


## 15. Quiz Flow
Student Opens Quiz
     ↓
API Returns Questions
without correct-answer information
     ↓
Student Selects Answers
     ↓
POST /quizzes/{id}/submit
     ↓
Backend Calculates Score
     ↓
QuizAttempt Created
     ↓
StudentAnswers Stored
     ↓
Result Returned

Correct answers must not be exposed to Students before submission.


## 16. AI Tutor Architecture
Student
  │
  ▼
React AI Chat
  │
  ▼
POST /api/v1/ai/chat
  │
  ▼
JWT Validation
  │
  ▼
Student Role Check
  │
  ▼

Course Exists?
  │
  ▼
Student Enrolled?
  │
  ▼
Retrieve Course Context
  │
  ▼
Vector Search
course_id filter
  │
  ▼
Relevant Lesson Chunks
  │
  ▼
Prompt + Context
  │
  ▼
LLM
  │
  ▼
AI Answer
  │
  ▼
Store Conversation
  │
  ▼
Return Response


## 17. AI Access Rule
An unenrolled Student must not be allowed to use the AI Tutor to access restricted course
material.

Example:

Student asks about Course 18
    ↓
Backend checks enrollment
    ↓
No Enrollment
    ↓
403 Forbidden

AI functionality must obey the same application authorization rules as normal LMS
functionality.


## 18. AI Data Isolation
AI retrieval should be filtered using:

course_id

Conceptually:

Retrieve semantically similar chunks

AND

course_id = requested_course

This prevents:

Python Course Question
     ↓
Accidentally retrieving Java Course material


## 19. AI Conversation Storage
Each AI conversation belongs to:

One Student
+
One Course

Example:

Student 15
Course 7
   │
   ▼
AIConversation 44
   │
   ├── USER message
   ├── ASSISTANT message
   ├── USER message
   └── ASSISTANT message

A Student cannot view another Student's AI conversations.


## 20. AI Quiz Generation Flow — Optional
Instructor
  │
  ▼
Select Lesson
  │
  ▼
Request AI Quiz
  │
  ▼
Backend validates ownership
  │
  ▼
Lesson Content
  │
  ▼
LLM
  │
  ▼
Draft Questions
  │
  ▼
Instructor Review
  │
  ├── Edit
  ├── Reject
  └── Approve
  │
  ▼
Save Quiz

AI-generated questions are never automatically published.


## 21. Failure Boundaries
Database Unavailable
Expected:

Database request fails
    ↓
Backend logs error
    ↓
503 Service Unavailable

The API should never return fake success.


Invalid JWT
Expected:

Invalid / Expired JWT
     ↓
401 Unauthorized


Insufficient Permission
Example:

Student → POST /courses

Expected:

403 Forbidden


Resource Does Not Exist
Example:

GET /courses/999999

Expected:

404 Not Found


Duplicate Enrollment
Expected:

409 Conflict

AI Provider Failure
Expected:

AI provider unavailable
     ↓
AI endpoint returns 503
     ↓
Core LMS remains operational

The LMS must not become unusable simply because the external AI provider is unavailable.


## 22. Architectural Principles
The reference architecture follows these principles:

## 1. React never talks directly to PostgreSQL.
## 2. Backend authorization is authoritative.
## 3. AI cannot bypass LMS permissions.
## 4. Relational data stays in PostgreSQL.
## 5. AI is an enhancement, not the foundation of the LMS.
## 6. Course context isolates AI retrieval.
## 7. Core LMS continues working when AI fails.
## 8. The MVP uses a modular monolith rather than unnecessary microservices.
## 9. Database constraints reinforce application rules.
   10.All externally visible operations are exposed through versioned REST APIs.
