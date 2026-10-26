import { useEffect,useState } from "react";
import { Link,useParams,useNavigate } from "react-router-dom";
import courseService from "../../services/courseService";
import CourseForm from "../../components/course/CourseForm";
import ModuleForm from "../../components/course/ModuleForm";
import LessonForm from "../../components/course/LessonForm";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";

export default function CourseEditor(){
  const {courseId}=useParams();const navigate=useNavigate();const [course,setCourse]=useState(null);const [modules,setModules]=useState([]);const [loading,setLoading]=useState(true);const [error,setError]=useState("");
  async function loadEditor(){try{setLoading(true);setError("");const courseData=await courseService.getCourse(courseId);const outline=await courseService.getCourseOutline(courseId);setCourse(courseData);setModules(outline);}catch(err){setError(err?.response?.data?.message||"Unable to load Course Editor.");}finally{setLoading(false);}}
  useEffect(()=>{loadEditor();},[courseId]);
  async function updateCourse(payload){setCourse(await courseService.updateCourse(courseId,payload));}
  async function publish(){try{setCourse(await courseService.publishCourse(courseId));}catch(err){setError(err?.response?.data?.message||"Unable to publish course.");}}
  async function addModule(payload){await courseService.createModule(courseId,payload);await loadEditor();}
  async function deleteModule(moduleId){if(!window.confirm("Delete this module?"))return;try{await courseService.deleteModule(moduleId);await loadEditor();}catch(err){setError(err?.response?.data?.message||"Unable to delete module.");}}
  async function addLesson(moduleId,payload){await courseService.createLesson(moduleId,payload);await loadEditor();}
  async function deleteLesson(lessonId){if(!window.confirm("Delete this lesson?"))return;try{await courseService.deleteLesson(lessonId);await loadEditor();}catch(err){setError(err?.response?.data?.message||"Unable to delete lesson.");}}
  async function deleteCourse(){if(!window.confirm("Delete this course? This action may not be reversible."))return;try{await courseService.deleteCourse(courseId);navigate("/instructor/dashboard");}catch(err){setError(err?.response?.data?.message||"Unable to delete course.");}}
  if(loading)return <LoadingSpinner text="Loading Course Editor..."/>;
  if(!course)return <ErrorState message={error||"Course could not be loaded."}/>;
  return <>{error&&<ErrorState message={error}/>}<div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-4"><div><h1 className="h2 mb-1">{course.title}</h1><span className={`badge ${course.status==="PUBLISHED"?"text-bg-success":"text-bg-secondary"}`}>{course.status}</span></div><div className="d-flex gap-2 flex-wrap">{course.status==="DRAFT"&&<button className="btn btn-success" onClick={publish}>Publish Course</button>}<Link to={`/instructor/courses/${courseId}/quiz`} className="btn btn-outline-primary">Quiz Manager</Link><Link to={`/instructor/courses/${courseId}/students`} className="btn btn-outline-primary">Students</Link><button className="btn btn-outline-danger" onClick={deleteCourse}>Delete Course</button></div></div><section className="card mb-4"><div className="card-body"><h2 className="h4">Course Information</h2><CourseForm initialValue={course} onSubmit={updateCourse} submitLabel="Update Course"/></div></section><section><div className="d-flex justify-content-between align-items-center mb-3"><h2 className="h4 mb-0">Modules & Lessons</h2></div>{modules.map(module=><div className="card mb-4" key={module.id}><div className="card-body"><div className="d-flex justify-content-between align-items-start"><div><h3 className="h5">{module.position}. {module.title}</h3><p className="text-secondary">{module.description}</p></div><button className="btn btn-outline-danger btn-sm" onClick={()=>deleteModule(module.id)}>Delete Module</button></div><div className="list-group mb-3">{(module.lessons||[]).map(lesson=><div key={lesson.id} className="list-group-item d-flex justify-content-between align-items-center"><span>{lesson.position}. {lesson.title}</span><button className="btn btn-outline-danger btn-sm" onClick={()=>deleteLesson(lesson.id)}>Delete</button></div>)}</div><LessonForm moduleId={module.id} defaultPosition={(module.lessons||[]).length+1} onSubmit={addLesson}/></div></div>)}<ModuleForm defaultPosition={modules.length+1} onSubmit={addModule}/></section></>;
}
