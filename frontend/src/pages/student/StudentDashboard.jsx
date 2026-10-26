import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import enrollmentService from "../../services/enrollmentService";
import quizService from "../../services/quizService";
import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";

export default function StudentDashboard(){
  const {user}=useAuth(); const [courses,setCourses]=useState([]); const [attempts,setAttempts]=useState([]); const [loading,setLoading]=useState(true);
  useEffect(()=>{async function load(){try{const [myCourses,myAttempts]=await Promise.all([enrollmentService.getMyCourses(),quizService.getMyAttempts()]);setCourses(myCourses);setAttempts(myAttempts.slice(0,5));}finally{setLoading(false);}}load();},[]);
  if(loading)return <LoadingSpinner text="Loading dashboard..." />;
  return <div><h1 className="h2">Welcome, {user.name}</h1><p className="text-secondary">Continue your learning.</p><hr/><h2 className="h4 mb-3">My Courses</h2>{courses.length===0?<EmptyState title="No Enrolled Courses" message="You are not enrolled in any courses yet." action={<Link to="/courses" className="btn btn-primary">Browse Courses</Link>}/>:<div className="row g-4">{courses.map(course=><div className="col-md-6" key={course.course_id}><CourseCard course={{id:course.course_id,title:course.title,status:course.status}} progress={course.progress_percentage} actionLabel="Continue" actionTo={`/courses/${course.course_id}`}/></div>)}</div>}<h2 className="h4 mt-5 mb-3">Recent Quiz Attempts</h2>{attempts.length===0?<p className="text-secondary">No quiz attempts yet.</p>:<div className="table-responsive"><table className="table"><thead><tr><th>Quiz</th><th>Score</th><th>Submitted</th></tr></thead><tbody>{attempts.map(attempt=><tr key={attempt.attempt_id}><td>{attempt.quiz_title}</td><td>{attempt.score}%</td><td>{new Date(attempt.submitted_at).toLocaleString()}</td></tr>)}</tbody></table></div>}</div>;
}
