from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Course, Lesson, LessonProgress, Module
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
)
from app.utils.responses import error, success
from app.utils.validators import positive_integer, required_string


modules_bp = Blueprint(
    "modules",
    __name__,
    url_prefix="/api/v1",
)


def _draft_course_visible_to_user(course, user):
    return bool(
        user
        and user.is_active
        and (
            user.role == "ADMIN"
            or is_course_owner(user, course)
        )
    )


@modules_bp.get("/courses/<int:course_id>/modules")
@jwt_required(optional=True)
def list_modules(course_id):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if course.status != "PUBLISHED":
        user = get_current_user()

        if not _draft_course_visible_to_user(course, user):
            return error(
                "COURSE_NOT_FOUND",
                "Course does not exist.",
                404,
            )

    return success([
        module.to_dict()
        for module in course.modules
    ])


@modules_bp.post("/courses/<int:course_id>/modules")
@roles_required("INSTRUCTOR")
def create_module(course_id, current_user):
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
    position = payload.get("position")

    if not required_string(title):
        return error(
            "VALIDATION_ERROR",
            "Module title is required.",
            400,
        )

    if not positive_integer(position):
        return error(
            "VALIDATION_ERROR",
            "Module position must be a positive integer.",
            400,
        )

    module = Module(
        course_id=course.id,
        title=title.strip(),
        description=description.strip()
        if isinstance(description, str)
        else None,
        position=position,
    )

    db.session.add(module)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return error(
            "MODULE_POSITION_CONFLICT",
            "Another module already uses this position.",
            409,
        )

    return success(module.to_dict(), 201)


@modules_bp.put("/modules/<int:module_id>")
@roles_required("INSTRUCTOR")
def update_module(module_id, current_user):
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

    if "title" in payload:
        if not required_string(payload["title"]):
            return error(
                "VALIDATION_ERROR",
                "Module title cannot be empty.",
                400,
            )
        module.title = payload["title"].strip()

    if "description" in payload:
        value = payload["description"]
        module.description = value.strip() if isinstance(value, str) else None

    if "position" in payload:
        if not positive_integer(payload["position"]):
            return error(
                "VALIDATION_ERROR",
                "Module position must be a positive integer.",
                400,
            )
        module.position = payload["position"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return error(
            "MODULE_POSITION_CONFLICT",
            "Another module already uses this position.",
            409,
        )

    return success(module.to_dict())


@modules_bp.delete("/modules/<int:module_id>")
@roles_required("INSTRUCTOR")
def delete_module(module_id, current_user):
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

    lesson_ids = [
        lesson.id
        for lesson in module.lessons
    ]

    if lesson_ids:
        has_progress = (
            LessonProgress.query
            .filter(
                LessonProgress.lesson_id.in_(lesson_ids)
            )
            .first()
            is not None
        )

        if has_progress:
            return error(
                "MODULE_HAS_LEARNER_DATA",
                "Module cannot be deleted after learner progress exists.",
                409,
            )

    db.session.delete(module)
    db.session.commit()

    return success({
        "module_id": module_id,
        "deleted": True,
    })
