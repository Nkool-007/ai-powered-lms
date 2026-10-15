from datetime import datetime, timezone

from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Course, Enrollment, Lesson, LessonProgress, User
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
)
from app.services.progress_service import calculate_course_progress
from app.utils.responses import error, success

progress_bp = Blueprint(
    "progress",
    __name__,
    url_prefix="/api/v1",
)


@progress_bp.post("/lessons/<int:lesson_id>/complete")
@roles_required("STUDENT")
def complete_lesson(lesson_id, current_user):
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return error(
            "LESSON_NOT_FOUND",
            "Lesson does not exist.",
            404,
        )

    course = lesson.module.course

    enrollment = (
        Enrollment.query
        .filter_by(
            student_id=current_user.id,
            course_id=course.id,
            status="ACTIVE",
        )
        .first()
    )

    if not enrollment:
        return error(
            "COURSE_ENROLLMENT_REQUIRED",
            "You must be enrolled in this course.",
            403,
        )

    progress = (
        LessonProgress.query
        .filter_by(
            student_id=current_user.id,
            lesson_id=lesson.id,
        )
        .first()
    )

    now = datetime.now(timezone.utc)

    if not progress:
        progress = LessonProgress(
            student_id=current_user.id,
            lesson_id=lesson.id,
            completed=True,
            completed_at=now,
            last_accessed_at=now,
        )
        db.session.add(progress)

    else:
        progress.last_accessed_at = now

        if not progress.completed:
            progress.completed = True
            progress.completed_at = now

    db.session.commit()

    return success(
        {
            "lesson_id": lesson.id,
            "completed": True,
            "completed_at": progress.completed_at.isoformat(),
        }
    )


@progress_bp.get("/courses/<int:course_id>/progress")
@roles_required("STUDENT")
def my_course_progress(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    enrollment = (
        Enrollment.query
        .filter_by(
            student_id=current_user.id,
            course_id=course.id,
        )
        .first()
    )

    if not enrollment:
        return error(
            "COURSE_ENROLLMENT_REQUIRED",
            "You must be enrolled in this course.",
            403,
        )

    return success(
        calculate_course_progress(
            current_user.id,
            course.id,
        )
    )


@progress_bp.get(
    "/courses/<int:course_id>/students/<int:student_id>/progress"
)
@jwt_required()
def instructor_student_progress(course_id, student_id):
    user = get_current_user()

    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if (
        not user
        or (
            user.role != "ADMIN"
            and not is_course_owner(user, course)
        )
    ):
        return error(
            "INSUFFICIENT_PERMISSION",
            "You cannot view progress for this course.",
            403,
        )

    student = db.session.get(User, student_id)

    if not student or student.role != "STUDENT":
        return error(
            "STUDENT_NOT_FOUND",
            "Student does not exist.",
            404,
        )

    enrollment = (
        Enrollment.query
        .filter_by(
            student_id=student.id,
            course_id=course.id,
        )
        .first()
    )

    if not enrollment:
        return error(
            "STUDENT_NOT_ENROLLED",
            "Student is not enrolled in this course.",
            404,
        )

    data = calculate_course_progress(
        student.id,
        course.id,
    )

    data["student_id"] = student.id

    return success(data)
