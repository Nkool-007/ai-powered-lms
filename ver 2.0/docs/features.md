# AI-Powered LMS — Feature Catalogue

## 1. Authentication & Authorization
        Feature                  Description                    Persona      Priority   MVP

User Registration       Create a new account              Student/Instruct   MUST       Yes
                                                          or

Login                   Authenticate existing users       All                MUST       Yes

Logout                  End authenticated session         All                MUST       Yes

Secure Password         Passwords must not be stored      All                MUST       Yes
Handling                as readable text

Student Role            Student-specific permissions      Student            MUST       Yes

Instructor Role         Instructor-specific permissions   Instructor         MUST       Yes

Admin Role              Administrative permissions        Admin              MUST       Yes

Protected               Restrict features to              All                MUST       Yes
Functionality           authenticated users

Role-Based              Restrict actions according to     All                MUST       Yes
Permissions             user role

Forgot Password         Account recovery workflow         All                SHOUL      No
                                                                             D

Social Login            Login using third-party           All                COULD      No
                        provider


## 2. Course Management
   Feature                      Description                     Persona      Priority   MVP

Create Course       Instructor creates a course           Instructor         MUST       Yes

Edit Course         Instructor modifies own course        Instructor         MUST       Yes

Delete Course       Instructor removes own course         Instructor         SHOUL      Yes
                    where permitted                                          D

Course Title        Name of course                        Instructor         MUST       Yes

Course              Overview of learning content          Instructor         MUST       Yes
**Description**

Course            Associate course with creator         Instructor        MUST       Yes
Instructor

Draft Status      Course can remain unpublished         Instructor        MUST       Yes
                  during development

Publish Course Make course available to students        Instructor        MUST       Yes

Unpublish         Remove course from public             Instructor/Admi   SHOUL      Yes
Course            availability                          n                 D

Course            Display available published courses   Student           MUST       Yes
Catalogue

Course Search     Search catalogue                      Student           SHOUL      No
                                                                          D

Course            Categorize courses                    Instructor        SHOUL      No
Category                                                                  D

Course Rating     Students rate courses                 Student           COULD      No


## 3. Module & Lesson Management
      Feature                 Description                Persona          Priority   MVP

Create Module         Divide course into sections   Instructor            MUST       Yes

Edit Module           Modify module details         Instructor            MUST       Yes

Delete Module         Remove unnecessary            Instructor            MUST       Yes
                      module

Module Ordering       Define module sequence        Instructor            MUST       Yes

Create Lesson         Add learning content          Instructor            MUST       Yes

Edit Lesson           Modify learning content       Instructor            MUST       Yes

Delete Lesson         Remove lesson                 Instructor            MUST       Yes

Lesson Ordering       Define lesson sequence        Instructor            MUST       Yes

Lesson Viewer         Student reads/views lesson    Student               MUST       Yes

Rich Media            Advanced media support        Student/Instructo     SHOULD     No
Lessons                                             r

## 4. Course Enrollment
       Feature                    Description              Persona        Priorit   MVP
                                                                            y

Enroll in Course         Student joins published course Student           MUST      Yes

Prevent Duplicate        Same student cannot enroll      Student/Syste    MUST      Yes
Enrollment               twice                           m

My Courses               Show student's enrollments      Student          MUST      Yes

View Enrolled Students   Instructor views learners in    Instructor       MUST      Yes
                         own course

Unenroll                 Student leaves course           Student          COUL      No
                                                                          D

Enrollment Approval      Instructor manually approves    Instructor       COUL      No
                         students                                         D


## 5. Learning & Content Delivery
       Feature                      Description              Person      Priority   MVP
                                                               a

Course Learning Page     Main page for enrolled course       Student     MUST       Yes

Module List              Show course modules                 Student     MUST       Yes

Lesson List              Show lessons under modules          Student     MUST       Yes

Lesson Access            Open permitted lesson               Student     MUST       Yes

Complete Lesson          Record lesson completion            Student     MUST       Yes

Continue Learning        Return quickly to incomplete        Student     SHOULD     No
                         course

Downloadable             Additional lesson resources         Student     SHOULD     No
Resources


## 6. Quiz & Assessment

         Feature                      Description               Persona     Priority    MVP

Create Quiz                  Instructor creates an              Instructo   MUST        Yes
                             assessment                         r

Create Question              Instructor adds quiz question      Instructo   MUST        Yes
                                                                r

Multiple-Choice Options      Provide possible answers           Instructo   MUST        Yes
                                                                r

Correct Answer               Store valid answer                 Instructo   MUST        Yes
                                                                r

Attempt Quiz                 Student answers assessment         Student     MUST        Yes

Submit Quiz                  Submit attempt for evaluation      Student     MUST        Yes

Score Calculation            Calculate result                   System      MUST        Yes

Store Quiz Attempt           Preserve assessment history        System      MUST        Yes

View Result                  Student sees score                 Student     MUST        Yes

Instructor Performance       Instructor sees student results    Instructo   SHOULD      No
View                                                            r

Question Explanation         Explain correct answer             Student     SHOULD      No


## 7. Progress Tracking
       Feature                    Description                  Persona       Priority   MVP

Lesson Completion         Record completed lessons       Student             MUST       Yes

Completed Lesson          Count completed lessons        Student             MUST       Yes
Count

Total Lesson Count        Count course lessons           Student             MUST       Yes

Completion                Calculate overall progress     Student             MUST       Yes
Percentage

Student Progress View     Student sees own progress      Student             MUST       Yes

Instructor Progress       Instructor sees learner        Instructor          MUST       Yes
View                      progress

Advanced Analytics         Detailed engagement           Instructor/Admi     COULD     No
                           analytics                     n


## 8. AI Features
           Feature                    Description           Person         Priority    MVP
                                                              a

AI Tutor                       Ask questions while         Student     MUST            Yes
                               learning

Explain Course Concepts        AI explains concepts        Student     MUST            Yes

Simplify Explanation           AI provides simpler         Student     MUST            Yes
                               explanation

Course-Relevant AI             Keep answers connected      Student     MUST            Yes
Responses                      to selected course

AI Quiz Generator              Generate draft quiz         Instructo   SHOULD          No
                               questions                   r

Human Review of AI             Instructor approves AI      Instructo   SHOULD          No
Questions                      content                     r

Weak Area Identification       Analyze areas needing       Student     COULD           No
                               improvement

Personalized Next-Step         Suggest next learning       Student     COULD           No
Recommendation                 activity

AI Citations/References        Show source lesson used     Student     COULD           No
                               by AI

Streaming AI Responses         Display AI output           Student     COULD           No
                               progressively

Multi-Agent Learning           Multiple specialized AI     Student     OUT OF          No
System                         agents                                  SCOPE


## 9. Admin Features
           Feature                     Description             Person       Priority   MVP
                                                                 a

 Admin Login                      Secure administrative access      Admin      MUST    Yes

 View Users                       List platform users               Admin      MUST    Yes

 View Courses                     List platform courses             Admin      MUST    Yes

 Disable User                     Restrict problematic account      Admin      SHOUL   No
                                                                               D

 Reactivate User                  Restore user account              Admin      SHOUL   No
                                                                               D

 Moderate Course                  Unpublish/remove invalid          Admin      SHOUL   No
                                  course                                       D

 Basic Platform Statistics        User/course/enrollment totals     Admin      SHOUL   No
                                                                               D

 Complex Analytics                Advanced business analytics       Admin      COULD   No
 Dashboard


## 10. Integration Features
        Feature                      Description          Person            Priority   MVP
                                                            a

 Email Notifications         Send selected system         All        SHOULD            No
                             emails

 Password Reset Email        Account recovery             All        SHOULD            No

 Google Login                Third-party authentication   All        COULD             No

 Real-Time Notifications     Live platform alerts         All        COULD             No

 Payment Gateway             Paid course marketplace      Student    OUT OF            No
                                                                     SCOPE

 Live Video Integration      Built-in live classes        All        OUT OF            No
                                                                     SCOPE


## 11. DevOps / Production Requirements
These are not end-user product features, but they are mandatory final capstone
requirements.

   Requirement                  Description           Priority         Final Project
                                                                       Requirement

Version Control      Maintain project repository      MUST       Yes

Database             Manage database changes          MUST       Yes
Migrations           safely

Automated Tests      Test important behavior          MUST       Yes

Dockerisation        Containerize application         MUST       Yes

Docker Compose       Run required services together   SHOUL      Recommended
                                                      D

Cloud Deployment     Deploy working application       MUST       Yes

Environment          Keep configuration/secrets       MUST       Yes
Variables            outside source

README               Professional project             MUST       Yes
                     documentation

API                  Document REST endpoints          SHOUL      Recommended
Documentation                                         D

CI/CD                Automate test/build pipeline     SHOUL      Recommended
                                                      D


## 12. MVP Feature Summary
The Mandatory MVP will contain:

## 1. User registration and login.
## 2. Student, Instructor and Admin roles.
## 3. Role-based access.
## 4. Course creation.
## 5. Course editing.
## 6. Modules.
## 7. Lessons.
## 8. Course publishing.
## 9. Course catalogue.
   10.Student enrollment.
   11.Duplicate enrollment prevention.
   12.My Courses.
   13.Lesson access.
   14.Lesson completion.

    15.Quiz creation.
    16.Quiz attempt.
    17.Automatic scoring.
    18.Progress tracking.
    19.Instructor progress visibility.
    20.Basic administration.
    21.Course-aware AI Tutor.
    22.AI-assisted explanations.
