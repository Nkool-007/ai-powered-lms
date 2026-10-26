import { useEffect,useMemo,useState } from "react";
import { Link,useParams } from "react-router-dom";
import courseService from "../../services/courseService";
import enrollmentService from "../../services/enrollmentService";
import LessonList from "../../components/lesson/LessonList";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";
import Button from "../../components/common/Button";

export default function LessonPage(){
  const {courseId,lessonId}=useParams();const [lesson,setLesson]=useState(null);const [modules,setModules]=useState([]);const [completed,setCompleted]=useState(false);const [loading,setLoading]=useState(true);const [completing,setCompleting]=useState(false);const [error,setError]=useState("");
  async function load(){try{setLoading(true);setError("");const [lessonData,outline]=await Promise.all([courseService.getLesson(lessonId),courseService.getCourseOutline(courseId)]);setLesson(lessonData);setModules(outline);}catch(err){setError(err?.response?.data?.message||"Unable to load lesson.");}finally{setLoading(false);}}
  useEffect(()=>{load();},[courseId,lessonId]);
  const lessons=useMemo(()=>modules.flatMap(module=>module.lessons||[]),[modules]);const currentIndex=lessons.findIndex(item=>item.id===Number(lessonId));const previousLesson=currentIndex>0?lessons[currentIndex-1]:null;const nextLesson=currentIndex>=0&&currentIndex<lessons.length-1?lessons[currentIndex+1]:null;
  async function complete(){try{setCompleting(true);setError("");await enrollmentService.completeLesson(lessonId);setCompleted(true);}catch(err){setError(err?.response?.data?.message||"Unable to complete lesson.");}finally{setCompleting(false);}}
  if(loading)return <LoadingSpinner text="Loading lesson..."/>;
  if(error&&!lesson)return <div className="container py-5"><ErrorState message={error} onRetry={load}/></div>;
  return <div className="container-fluid py-4"><div className="row g-4"><aside className="col-lg-3"><LessonList courseId={courseId} modules={modules} currentLessonId={lessonId} completedIds={completed?[Number(lessonId)]:[]}/></aside><article className="col-lg-9">{error&&<ErrorState message={error}/>}<h1>{lesson.title}</h1><div className="lesson-content my-4">{lesson.content}</div><Button variant={completed?"success":"primary"} loading={completing} disabled={completed} onClick={complete}>{completed?"Completed":"Mark as Complete"}</Button><div className="d-flex justify-content-between mt-5">{previousLesson?<Link className="btn btn-outline-secondary" to={`/courses/${courseId}/lessons/${previousLesson.id}`}>← Previous</Link>:<span/>}{nextLesson&&<Link className="btn btn-primary" to={`/courses/${courseId}/lessons/${nextLesson.id}`}>Next →</Link>}</div></article></div></div>;
}
