import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import enrollmentService from "../../services/enrollmentService";
import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";

export default function MyCourses(){
  const [courses,setCourses]=useState([]);const [loading,setLoading]=useState(true);
  useEffect(()=>{enrollmentService.getMyCourses().then(setCourses).finally(()=>setLoading(false));},[]);
  if(loading)return <LoadingSpinner text="Loading your courses..."/>;
  if(courses.length===0)return <EmptyState title="No Enrolled Courses" message="Start by exploring the course catalog." action={<Link to="/courses" className="btn btn-primary">Browse Courses</Link>}/>;
  return <><h1 className="h2 mb-4">My Courses</h1><div className="row g-4">{courses.map(course=><div className="col-md-6 col-xl-4" key={course.course_id}><CourseCard course={{id:course.course_id,title:course.title,status:course.status}} progress={course.progress_percentage} actionLabel="Continue Learning"/></div>)}</div></>;
}
