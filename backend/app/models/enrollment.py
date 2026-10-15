from app.extensions import db
from app.models.base import BIGINT


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(BIGINT, primary_key=True)

    student_id = db.Column(
        BIGINT,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    course_id = db.Column(
        BIGINT,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVE",
    )

    enrolled_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_enrollment_student_course",
        ),
        db.CheckConstraint(
            "status IN ('ACTIVE', 'COMPLETED')",
            name="ck_enrollment_status",
        ),
    )

    student = db.relationship(
        "User",
        back_populates="enrollments",
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments",
    )
