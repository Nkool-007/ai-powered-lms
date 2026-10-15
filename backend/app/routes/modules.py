from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Course, LessonProgress, Module
from app.models.lesson import Lesson
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
)
from app.utils.responses import error, success
from app.utils.validators import required_string

modules_bp = Blueprint(
    "modules",
    __name__,
    url_prefix="/api/v1",
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

    if course.status == "DRAFT":
        user = get_current_user()

        if not user or not is_course_owner(user, course):
            return error(
                "COURSE_ACCESS_DENIED",
                "This course is not publicly available.",
                403,
            )

    return success([module.to_dict() for module in course.modules])


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

    if (
        not required_string(title)
        or not isinstance(position, int)
        or position < 1
    ):
        return error(
            "VALIDATION_ERROR",
            "Valid title and positive position are required.",
            400,
        )

    module = Module(
        course_id=course.id,
        title=title.strip(),
        description=(
            description.strip()
            if isinstance(description, str)
            else None
        ),
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
            "You cannot modify this module.",
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
        module.description = (
            payload["description"].strip()
            if isinstance(payload["description"], str)
            else None
        )

    if "position" in payload:
        position = payload["position"]

        if not isinstance(position, int) or position < 1:
            return error(
                "VALIDATION_ERROR",
                "Position must be a positive integer.",
                400,
            )

        module.position = position

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
            "You cannot modify this module.",
            403,
        )

    learner_progress = (
        LessonProgress.query
        .join(Lesson)
        .filter(Lesson.module_id == module.id)
        .first()
    )

    if learner_progress:
        return error(
            "MODULE_HAS_LEARNER_DATA",
            "This module cannot be deleted because learner progress exists.",
            409,
        )

    db.session.delete(module)
    db.session.commit()

    return "", 204
