from app.models import Enrollment, Lesson, LessonProgress, Module, Quiz, QuizAttempt
from app.ai.retriever.course_retriever import CourseRetriever


def require_enrollment(*, student_id, course_id):
    enrollment = (
        Enrollment.query
        .filter_by(student_id=student_id, course_id=course_id, status="ACTIVE")
        .first()
    )
    if not enrollment:
        raise PermissionError("Student is not enrolled in this Course.")


def search_course_content(*, student_id, course_id, query):
    require_enrollment(student_id=student_id, course_id=course_id)
    return CourseRetriever().retrieve(
        course_id=course_id,
        query=query,
        user_id=student_id,
    )


def get_student_progress(*, student_id, course_id):
    require_enrollment(student_id=student_id, course_id=course_id)

    total = (
        Lesson.query
        .join(Module)
        .filter(Module.course_id == course_id)
        .count()
    )

    completed = (
        LessonProgress.query
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .filter(
            LessonProgress.student_id == student_id,
            LessonProgress.completed.is_(True),
            Module.course_id == course_id,
        )
        .count()
    )

    percentage = round(completed / total * 100, 2) if total else 0
    return {
        "completed_lessons": completed,
        "total_lessons": total,
        "progress_percentage": percentage,
    }


def get_quiz_performance(*, student_id, course_id):
    require_enrollment(student_id=student_id, course_id=course_id)

    attempts = (
        QuizAttempt.query
        .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
        .filter(
            QuizAttempt.student_id == student_id,
            Quiz.course_id == course_id,
        )
        .order_by(QuizAttempt.submitted_at.desc())
        .all()
    )

    return [
        {
            "quiz_id": attempt.quiz_id,
            "score": float(attempt.score),
            "submitted_at": attempt.submitted_at.isoformat(),
        }
        for attempt in attempts
    ]


def get_course_structure(*, student_id, course_id):
    require_enrollment(student_id=student_id, course_id=course_id)

    modules = (
        Module.query
        .filter_by(course_id=course_id)
        .order_by(Module.position.asc())
        .all()
    )

    result = []
    for module in modules:
        lessons = (
            Lesson.query
            .filter_by(module_id=module.id)
            .order_by(Lesson.position.asc())
            .all()
        )
        result.append({
            "module_id": module.id,
            "module_title": module.title,
            "lessons": [
                {
                    "lesson_id": lesson.id,
                    "lesson_title": lesson.title,
                    "position": lesson.position,
                }
                for lesson in lessons
            ],
        })

    return result
