import { Route, Routes } from "react-router-dom";

import AppLayout from "./layouts/AppLayout";
import DashboardLayout from "./layouts/DashboardLayout";
import ProtectedRoute from "./routes/ProtectedRoute";

import Home from "./pages/public/Home";
import Login from "./pages/public/Login";
import Register from "./pages/public/Register";
import Courses from "./pages/public/Courses";
import CoursePage from "./pages/public/CoursePage";
import Forbidden from "./pages/public/Forbidden";
import NotFound from "./pages/public/NotFound";

import StudentDashboard from "./pages/student/StudentDashboard";
import MyCourses from "./pages/student/MyCourses";
import LessonPage from "./pages/student/LessonPage";
import QuizPage from "./pages/student/QuizPage";
import ProgressDashboard from "./pages/student/ProgressDashboard";
import AITutor from "./pages/student/AITutor";

import InstructorDashboard from "./pages/instructor/InstructorDashboard";
import CreateCourse from "./pages/instructor/CreateCourse";
import CourseEditor from "./pages/instructor/CourseEditor";
import QuizManager from "./pages/instructor/QuizManager";
import StudentProgress from "./pages/instructor/StudentProgress";
import AIQuizGenerator from "./pages/instructor/AIQuizGenerator";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/courses/:courseId" element={<CoursePage />} />

        <Route element={<ProtectedRoute allowedRoles={["STUDENT"]} />}>
          <Route element={<DashboardLayout role="STUDENT" />}>
            <Route path="/student/dashboard" element={<StudentDashboard />} />
            <Route path="/student/courses" element={<MyCourses />} />
            <Route path="/student/progress" element={<ProgressDashboard />} />
            <Route path="/student/ai" element={<AITutor />} />
          </Route>
          <Route path="/courses/:courseId/lessons/:lessonId" element={<LessonPage />} />
          <Route path="/quizzes/:quizId" element={<QuizPage />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["INSTRUCTOR"]} />}>
          <Route element={<DashboardLayout role="INSTRUCTOR" />}>
            <Route path="/instructor/dashboard" element={<InstructorDashboard />} />
            <Route path="/instructor/courses/new" element={<CreateCourse />} />
            <Route path="/instructor/courses/:courseId/edit" element={<CourseEditor />} />
            <Route path="/instructor/courses/:courseId/quiz" element={<QuizManager />} />
            <Route path="/instructor/courses/:courseId/students" element={<StudentProgress />} />
            <Route path="/instructor/ai-quiz" element={<AIQuizGenerator />} />
          </Route>
        </Route>

        <Route path="/forbidden" element={<Forbidden />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
