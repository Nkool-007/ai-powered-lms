from app.models import Lesson, LessonProgress, Module


def calculate_course_progress(student_id, course_id):
    total_lessons = (
        Lesson.query
        .join(Module)
        .filter(Module.course_id == course_id)
        .count()
    )

    completed_lessons = (
        LessonProgress.query
        .join(
            Lesson,
            Lesson.id == LessonProgress.lesson_id,
        )
        .join(
            Module,
            Module.id == Lesson.module_id,
        )
        .filter(
            LessonProgress.student_id == student_id,
            LessonProgress.completed.is_(True),
            Module.course_id == course_id,
        )
        .count()
    )

    if total_lessons == 0:
        percentage = 0
    else:
        percentage = round(
            (completed_lessons / total_lessons) * 100,
            2,
        )

    return {
        "course_id": course_id,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "progress_percentage": percentage,
    }
