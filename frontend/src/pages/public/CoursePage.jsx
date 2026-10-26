import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import courseService from "../../services/courseService";
import enrollmentService from "../../services/enrollmentService";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";
import Button from "../../components/common/Button";

export default function CoursePage() {
  const { courseId } = useParams(); const { user, isAuthenticated } = useAuth();
  const [course,setCourse]=useState(null); const [modules,setModules]=useState([]); const [enrolled,setEnrolled]=useState(false); const [loading,setLoading]=useState(true); const [enrolling,setEnrolling]=useState(false); const [error,setError]=useState("");
  async function load(){try{setLoading(true);setError("");const [courseData,outline]=await Promise.all([courseService.getCourse(courseId),courseService.getCourseOutline(courseId)]);setCourse(courseData);setModules(outline);if(user?.role==="STUDENT"){const myCourses=await enrollmentService.getMyCourses();setEnrolled(myCourses.some(item=>Number(item.course_id)===Number(courseId)));}}catch(err){setError(err?.response?.data?.message||"Unable to load course.");}finally{setLoading(false);}}
  useEffect(()=>{load();},[courseId,user?.id]);
  async function handleEnroll(){try{setEnrolling(true);await enrollmentService.enroll(courseId);setEnrolled(true);}catch(err){if(err?.response?.data?.error==="ALREADY_ENROLLED"){setEnrolled(true);return;}setError(err?.response?.data?.message||"Enrollment failed.");}finally{setEnrolling(false);}}
  if(loading)return <LoadingSpinner text="Loading course..." />;
  if(error&&!course)return <div className="container py-5"><ErrorState message={error} onRetry={load}/></div>;
  const firstLesson=modules.flatMap(module=>module.lessons||[])[0];
  return <div className="container py-5">{error&&<ErrorState message={error}/>}<div className="row g-5"><div className="col-lg-8"><h1>{course.title}</h1><p className="lead">{course.description}</p>{course.instructor&&<p className="text-secondary">Instructor: {course.instructor.name}</p>}<h2 className="h4 mt-5">Course Content</h2>{modules.map(module=><div key={module.id} className="card mb-3"><div className="card-body"><h3 className="h5">{module.position}. {module.title}</h3><p className="text-secondary">{module.description}</p><div className="list-group">{(module.lessons||[]).map(lesson=><div key={lesson.id} className="list-group-item">{lesson.position}. {lesson.title}</div>)}</div></div></div>)}</div><aside className="col-lg-4"><div className="card shadow-sm sticky-lg-top course-action-card"><div className="card-body">{!isAuthenticated&&<Link to="/login" className="btn btn-primary w-100">Login to Enroll</Link>}{user?.role==="STUDENT"&&!enrolled&&<Button className="w-100" loading={enrolling} onClick={handleEnroll}>Enroll</Button>}{user?.role==="STUDENT"&&enrolled&&firstLesson&&<Link to={`/courses/${courseId}/lessons/${firstLesson.id}`} className="btn btn-success w-100">Continue Learning</Link>}{user?.role==="INSTRUCTOR"&&course.instructor_id===user.id&&<Link to={`/instructor/courses/${courseId}/edit`} className="btn btn-primary w-100">Manage Course</Link>}</div></div></aside></div></div>;
}
