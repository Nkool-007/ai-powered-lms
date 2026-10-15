from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Course, Enrollment, Quiz, QuizAttempt
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
)
from app.utils.responses import error, success
from app.utils.validators import required_string

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/v1",
)


@courses_bp.get("/courses")
def list_courses():
    courses = (
        Course.query
        .filter_by(status="PUBLISHED")
        .order_by(Course.created_at.desc())
        .all()
    )

    return success([course.to_dict() for course in courses])


@courses_bp.get("/courses/<int:course_id>")
@jwt_required(optional=True)
def get_course(course_id):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if course.status == "DRAFT":
        user = get_current_user()

        if not user or not is_course_owner(user, course):
            return error(
                "COURSE_ACCESS_DENIED",
                "This course is not publicly available.",
                403,
            )

    return success(course.to_dict())


@courses_bp.post("/courses")
@roles_required("INSTRUCTOR")
def create_course(current_user):
    payload = request.get_json(silent=True) or {}

    title = payload.get("title")
    description = payload.get("description")

    if not required_string(title):
        return error(
            "VALIDATION_ERROR",
            "Course title is required.",
            400,
        )

    if not required_string(description):
        return error(
            "VALIDATION_ERROR",
            "Course description is required.",
            400,
        )

    course = Course(
        title=title.strip(),
        description=description.strip(),
        instructor_id=current_user.id,
        status="DRAFT",
    )

    db.session.add(course)
    db.session.commit()

    return success(course.to_dict(), 201)


@courses_bp.put("/courses/<int:course_id>")
@roles_required("INSTRUCTOR")
def update_course(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if not is_course_owner(current_user, course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot modify another instructor's course.",
            403,
        )

    payload = request.get_json(silent=True) or {}

    title = payload.get("title")
    description = payload.get("description")

    if title is not None:
        if not required_string(title):
            return error(
                "VALIDATION_ERROR",
                "Course title cannot be empty.",
                400,
            )
        course.title = title.strip()

    if description is not None:
        if not required_string(description):
            return error(
                "VALIDATION_ERROR",
                "Course description cannot be empty.",
                400,
            )
        course.description = description.strip()

    db.session.commit()
    return success(course.to_dict())


@courses_bp.patch("/courses/<int:course_id>/publish")
@roles_required("INSTRUCTOR")
def publish_course(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if not is_course_owner(current_user, course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot publish another instructor's course.",
            403,
        )

    if not course.modules:
        return error(
            "COURSE_NOT_READY",
            "Add at least one module before publishing.",
            409,
        )

    if not any(module.lessons for module in course.modules):
        return error(
            "COURSE_NOT_READY",
            "Add at least one lesson before publishing.",
            409,
        )

    course.status = "PUBLISHED"

    if not course.published_at:
        course.published_at = datetime.now(timezone.utc)

    db.session.commit()
    return success(course.to_dict())


@courses_bp.delete("/courses/<int:course_id>")
@roles_required("INSTRUCTOR")
def delete_course(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if not is_course_owner(current_user, course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot delete another instructor's course.",
            403,
        )

    has_enrollment = (
        Enrollment.query
        .filter_by(course_id=course.id)
        .first()
    )

    has_attempt = (
        QuizAttempt.query
        .join(Quiz)
        .filter(Quiz.course_id == course.id)
        .first()
    )

    if has_enrollment or has_attempt:
        return error(
            "COURSE_HAS_LEARNER_DATA",
            "Published learner history prevents destructive deletion. Unpublish the course instead.",
            409,
        )

    db.session.delete(course)
    db.session.commit()

    return "", 204


@courses_bp.get("/instructor/courses")
@roles_required("INSTRUCTOR")
def instructor_courses(current_user):
    courses = (
        Course.query
        .filter_by(instructor_id=current_user.id)
        .order_by(Course.created_at.desc())
        .all()
    )

    return success([course.to_dict() for course in courses])
