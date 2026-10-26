import { useEffect, useState } from "react";
import courseService from "../../services/courseService";
import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";
import EmptyState from "../../components/common/EmptyState";

export default function Courses() {
  const [courses,setCourses]=useState([]); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  async function loadCourses(){try{setLoading(true);setError("");setCourses(await courseService.getCourses());}catch{setError("Unable to load courses.");}finally{setLoading(false);}}
  useEffect(()=>{loadCourses();},[]);
  if(loading) return <LoadingSpinner text="Loading courses..." />;
  return <div className="container py-5"><div className="mb-4"><h1>Course Catalog</h1><p className="text-secondary">Explore published courses available on SmartLMS.</p></div>{error && <ErrorState message={error} onRetry={loadCourses} />}{!error && courses.length===0 && <EmptyState title="No Courses" message="No courses are currently available." />}<div className="row g-4">{courses.map(course=><div className="col-md-6 col-xl-4" key={course.id}><CourseCard course={course} /></div>)}</div></div>;
}
