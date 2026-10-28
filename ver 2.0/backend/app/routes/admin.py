from flask import Blueprint

from app.models import Course, User
from app.services.authorization import roles_required
from app.utils.responses import success


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/v1/admin",
)


@admin_bp.get("/users")
@roles_required("ADMIN")
def users(current_user):
    users = (
        User.query
        .order_by(User.created_at.desc())
        .all()
    )

    return success([
        user.to_dict()
        for user in users
    ])


@admin_bp.get("/courses")
@roles_required("ADMIN")
def courses(current_user):
    courses = (
        Course.query
        .order_by(Course.created_at.desc())
        .all()
    )

    return success([
        course.to_dict()
        for course in courses
    ])
