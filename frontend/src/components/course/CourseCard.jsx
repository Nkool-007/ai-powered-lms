import { Link } from "react-router-dom";
import ProgressBar from "../progress/ProgressBar";

export default function CourseCard({ course, actionLabel = "View Course", actionTo, progress }) {
  return (
    <article className="card h-100 shadow-sm course-card">
      <div className="card-body d-flex flex-column">
        <div className="d-flex justify-content-between gap-2">
          <h3 className="h5">{course.title}</h3>
          {course.status && <span className={`badge ${course.status === "PUBLISHED" ? "text-bg-success" : "text-bg-secondary"}`}>{course.status}</span>}
        </div>
        {course.instructor && <p className="small text-secondary">Instructor: {course.instructor.name}</p>}
        {course.description && <p className="text-secondary flex-grow-1">{course.description}</p>}
        {progress !== undefined && <div className="mb-3"><ProgressBar percentage={progress} /></div>}
        <Link to={actionTo || `/courses/${course.id}`} className="btn btn-primary">{actionLabel}</Link>
      </div>
    </article>
  );
}
