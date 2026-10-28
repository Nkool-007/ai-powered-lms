from flask import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Course, Enrollment
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
)
from app.services.progress_service import calculate_course_progress
from app.utils.responses import error, success
from app.utils.serialization import isoformat_or_none


enrollments_bp = Blueprint(
    "enrollments",
    __name__,
    url_prefix="/api/v1",
)


@enrollments_bp.post("/courses/<int:course_id>/enroll")
@roles_required("STUDENT")
def enroll(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if course.status != "PUBLISHED":
        return error(
            "COURSE_NOT_AVAILABLE",
            "Only published courses can be enrolled in.",
            403,
        )

    existing = (
        Enrollment.query
        .filter_by(
            student_id=current_user.id,
            course_id=course.id,
        )
        .first()
    )

    if existing:
        return error(
            "ALREADY_ENROLLED",
            "Student is already enrolled in this course.",
            409,
        )

    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course.id,
        status="ACTIVE",
    )

    db.session.add(enrollment)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return error(
            "ALREADY_ENROLLED",
            "Student is already enrolled in this course.",
            409,
        )

    return success({
        "course_id": course.id,
        "status": enrollment.status,
        "message": "Enrollment successful.",
    }, 201)


@enrollments_bp.get("/students/me/courses")
@roles_required("STUDENT")
def my_courses(current_user):
    enrollments = (
        Enrollment.query
        .filter_by(student_id=current_user.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )

    data = []

    for enrollment in enrollments:
        course = enrollment.course
        progress = calculate_course_progress(
            current_user.id,
            course.id,
        )

        data.append({
            "course_id": course.id,
            "title": course.title,
            "description": course.description,
            "status": enrollment.status,
            "enrolled_at": isoformat_or_none(enrollment.enrolled_at),
            "completed_at": isoformat_or_none(enrollment.completed_at),
            "progress_percentage": progress["progress_percentage"],
            "course": course.to_dict(),
        })

    return success(data)


@enrollments_bp.get("/courses/<int:course_id>/students")
@jwt_required()
def course_students(course_id):
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

    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    allowed = (
        user.role == "ADMIN"
        or is_course_owner(user, course)
    )

    if not allowed:
        return error(
            "INSUFFICIENT_PERMISSION",
            "You cannot view enrollments for this course.",
            403,
        )

    data = []

    for enrollment in course.enrollments:
        data.append({
            "student": {
                "id": enrollment.student.id,
                "name": enrollment.student.name,
                "email": enrollment.student.email,
            },
            "student_id": enrollment.student.id,
            "enrolled_at": isoformat_or_none(enrollment.enrolled_at),
            "completed_at": isoformat_or_none(enrollment.completed_at),
            "status": enrollment.status,
            "progress": calculate_course_progress(
                enrollment.student.id,
                course.id,
            ),
        })

    return success(data)
