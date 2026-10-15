from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import User
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


def roles_required(*roles):
    def decorator(function):
        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if not user:
                return error(
                    "USER_NOT_FOUND",
                    "Authenticated user does not exist.",
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
                    "You are not permitted to perform this action.",
                    403,
                )

            return function(
                *args,
                current_user=user,
                **kwargs,
            )

        return wrapper

    return decorator


def is_course_owner(user, course):
    return (
        user.role == "INSTRUCTOR"
        and course.instructor_id == user.id
    )
