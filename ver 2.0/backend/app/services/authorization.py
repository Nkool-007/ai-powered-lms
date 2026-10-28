from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Enrollment, User
from app.utils.responses import error


def get_current_user():
    identity = get_jwt_identity()

    if identity is None:
        return None

    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return None

    return db.session.get(User, user_id)


def is_course_owner(user, course):
    return (
        user is not None
        and user.role == "INSTRUCTOR"
        and course.instructor_id == user.id
    )


def student_has_course_access(student_id, course_id):
    return (
        Enrollment.query
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.status.in_(["ACTIVE", "COMPLETED"]),
        )
        .first()
        is not None
    )


def roles_required(*roles):
    def decorator(function):
        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):
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

            if user.role not in roles:
                return error(
                    "INSUFFICIENT_PERMISSION",
                    "You do not have permission to perform this action.",
                    403,
                )

            return function(
                *args,
                current_user=user,
                **kwargs,
            )

        return wrapper

    return decorator
