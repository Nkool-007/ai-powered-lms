from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Lesson, LessonProgress, Module
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
    student_has_course_access,
)
from app.utils.responses import error, success
from app.utils.validators import positive_integer, required_string


lessons_bp = Blueprint(
    "lessons",
    __name__,
    url_prefix="/api/v1",
)


@lessons_bp.get("/modules/<int:module_id>/lessons")
@jwt_required(optional=True)
def list_lessons(module_id):
    module = db.session.get(Module, module_id)

    if not module:
        return error(
            "MODULE_NOT_FOUND",
            "Module does not exist.",
            404,
        )

    course = module.course
    user = get_current_user()

    if course.status != "PUBLISHED":
        allowed = bool(
            user
            and user.is_active
            and (
                user.role == "ADMIN"
                or is_course_owner(user, course)
            )
        )

        if not allowed:
            return error(
                "MODULE_NOT_FOUND",
                "Module does not exist.",
                404,
            )

    include_content = bool(
        user
        and user.is_active
        and (
            user.role == "ADMIN"
            or is_course_owner(user, course)
        )
    )

    return success([
        lesson.to_dict(
            include_content=include_content
        )
        for lesson in module.lessons
    ])


@lessons_bp.post("/modules/<int:module_id>/lessons")
@roles_required("INSTRUCTOR")
def create_lesson(module_id, current_user):
    module = db.session.get(Module, module_id)

    if not module:
        return error(
            "MODULE_NOT_FOUND",
            "Module does not exist.",
            404,
        )

    if not is_course_owner(current_user, module.course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot modify another instructor's course.",
            403,
        )

    payload = request.get_json(silent=True) or {}

    title = payload.get("title")
    content = payload.get("content")
    position = payload.get("position")

    if not required_string(title):
        return error(
            "VALIDATION_ERROR",
            "Lesson title is required.",
            400,
        )

    if not required_string(content):
        return error(
            "VALIDATION_ERROR",
            "Lesson content is required.",
            400,
        )

    if not positive_integer(position):
        return error(
            "VALIDATION_ERROR",
            "Lesson position must be a positive integer.",
            400,
        )

    lesson = Lesson(
        module_id=module.id,
        title=title.strip(),
        content=content.strip(),
        position=position,
    )

    db.session.add(lesson)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return error(
            "LESSON_POSITION_CONFLICT",
            "Another lesson already uses this position.",
            409,
        )

    return success(lesson.to_dict(), 201)


@lessons_bp.get("/lessons/<int:lesson_id>")
@jwt_required()
def get_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return error(
            "LESSON_NOT_FOUND",
            "Lesson does not exist.",
            404,
        )

    user = get_current_user()

    if not user:
        return error(
            "AUTHENTICATION_REQUIRED",
            "Authentication is required.",
            401,
        )

    if not user.is_active:
        return error(
            "ACCOUNT_DISABLED",
            "This account has been disabled.",
            403,
        )

    course = lesson.module.course

    if user.role == "STUDENT":
        if not student_has_course_access(
            user.id,
            course.id,
        ):
            return error(
                "COURSE_ENROLLMENT_REQUIRED",
                "You must be enrolled in this course.",
                403,
            )

    elif user.role == "INSTRUCTOR":
        if not is_course_owner(user, course):
            return error(
                "NOT_COURSE_OWNER",
                "You cannot access another instructor's lesson.",
                403,
            )

    elif user.role != "ADMIN":
        return error(
            "INSUFFICIENT_PERMISSION",
            "You do not have permission to access this lesson.",
            403,
        )

    return success(lesson.to_dict(include_content=True))


@lessons_bp.put("/lessons/<int:lesson_id>")
@roles_required("INSTRUCTOR")
def update_lesson(lesson_id, current_user):
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return error(
            "LESSON_NOT_FOUND",
            "Lesson does not exist.",
            404,
        )

    if not is_course_owner(
        current_user,
        lesson.module.course,
    ):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot modify another instructor's course.",
            403,
        )

    payload = request.get_json(silent=True) or {}

    if "title" in payload:
        if not required_string(payload["title"]):
            return error(
                "VALIDATION_ERROR",
                "Lesson title cannot be empty.",
                400,
            )
        lesson.title = payload["title"].strip()

    if "content" in payload:
        if not required_string(payload["content"]):
            return error(
                "VALIDATION_ERROR",
                "Lesson content cannot be empty.",
                400,
            )
        lesson.content = payload["content"].strip()

    if "position" in payload:
        if not positive_integer(payload["position"]):
            return error(
                "VALIDATION_ERROR",
                "Lesson position must be a positive integer.",
                400,
            )
        lesson.position = payload["position"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return error(
            "LESSON_POSITION_CONFLICT",
            "Another lesson already uses this position.",
            409,
        )

    return success(lesson.to_dict())


@lessons_bp.delete("/lessons/<int:lesson_id>")
@roles_required("INSTRUCTOR")
def delete_lesson(lesson_id, current_user):
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return error(
            "LESSON_NOT_FOUND",
            "Lesson does not exist.",
            404,
        )

    if not is_course_owner(
        current_user,
        lesson.module.course,
    ):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot modify another instructor's course.",
            403,
        )

    has_progress = (
        LessonProgress.query
        .filter_by(lesson_id=lesson.id)
        .first()
        is not None
    )

    if has_progress:
        return error(
            "LESSON_HAS_LEARNER_DATA",
            "Lesson cannot be deleted after learner progress exists.",
            409,
        )

    db.session.delete(lesson)
    db.session.commit()

    return success({
        "lesson_id": lesson_id,
        "deleted": True,
    })
