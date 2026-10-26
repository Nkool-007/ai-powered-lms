import { useEffect,useState } from "react";
import { useParams } from "react-router-dom";
import courseService from "../../services/courseService";
import ProgressBar from "../../components/progress/ProgressBar";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";

export default function StudentProgress(){
  const {courseId}=useParams();const [students,setStudents]=useState([]);const [selectedProgress,setSelectedProgress]=useState(null);const [loading,setLoading]=useState(true);const [error,setError]=useState("");
  useEffect(()=>{courseService.getCourseStudents(courseId).then(setStudents).catch(err=>setError(err?.response?.data?.message||"Unable to load students.")).finally(()=>setLoading(false));},[courseId]);
  async function viewProgress(studentId){try{setError("");setSelectedProgress(await courseService.getStudentProgress(courseId,studentId));}catch(err){setError(err?.response?.data?.message||"Unable to load progress.");}}
  if(loading)return <LoadingSpinner text="Loading students..."/>;
  return <><h1 className="h2">Student Progress</h1>{error&&<ErrorState message={error}/>} {students.length===0?<EmptyState title="No Students" message="No students are enrolled in this course yet."/>:<div className="table-responsive mt-4"><table className="table align-middle"><thead><tr><th>Student</th><th>Email</th><th>Status</th><th/></tr></thead><tbody>{students.map(entry=><tr key={entry.student.id}><td>{entry.student.name}</td><td>{entry.student.email}</td><td>{entry.status}</td><td><button className="btn btn-outline-primary btn-sm" onClick={()=>viewProgress(entry.student.id)}>View Progress</button></td></tr>)}</tbody></table></div>}{selectedProgress&&<div className="card mt-4"><div className="card-body"><h2 className="h5">Student {selectedProgress.student_id}</h2><ProgressBar percentage={selectedProgress.progress_percentage}/><p className="mt-3 mb-0">{selectedProgress.completed_lessons} of {selectedProgress.total_lessons} lessons completed.</p></div></div>}</>;
}
