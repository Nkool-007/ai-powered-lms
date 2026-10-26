import { Link } from "react-router-dom";

export default function LessonList({ courseId, modules = [], currentLessonId, completedIds = [] }) {
  return (
    <div>
      {modules.map((module) => (
        <section key={module.id} className="mb-4">
          <h3 className="h6">{module.position}. {module.title}</h3>
          <div className="list-group">
            {(module.lessons || []).map((lesson) => {
              const completed = completedIds.includes(lesson.id);
              const current = Number(currentLessonId) === lesson.id;
              return (
                <Link key={lesson.id} to={`/courses/${courseId}/lessons/${lesson.id}`} className={`list-group-item list-group-item-action ${current ? "active" : ""}`}>
                  <span className="me-2">{completed ? "✓" : current ? "●" : "○"}</span>{lesson.title}
                </Link>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
}
