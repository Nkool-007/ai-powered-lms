from app.extensions import db
from app.models.base import ID_TYPE
from app.utils.serialization import isoformat_or_none


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(ID_TYPE, primary_key=True)
    student_id = db.Column(
        ID_TYPE,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    course_id = db.Column(
        ID_TYPE,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )
    status = db.Column(db.String(20), nullable=False, default="ACTIVE")
    enrolled_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_enrollments_student_course",
        ),
        db.CheckConstraint(
            "status IN ('ACTIVE', 'COMPLETED')",
            name="ck_enrollments_status",
        ),
    )

    student = db.relationship(
        "User",
        back_populates="enrollments",
        foreign_keys=[student_id],
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "status": self.status,
            "enrolled_at": isoformat_or_none(self.enrolled_at),
            "completed_at": isoformat_or_none(self.completed_at),
        }
