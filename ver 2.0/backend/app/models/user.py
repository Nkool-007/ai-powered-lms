from app.extensions import db
from app.models.base import ID_TYPE, TimestampMixin
from app.utils.serialization import isoformat_or_none


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(ID_TYPE, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        db.CheckConstraint(
            "role IN ('STUDENT', 'INSTRUCTOR', 'ADMIN')",
            name="ck_users_role",
        ),
    )

    courses = db.relationship(
        "Course",
        back_populates="instructor",
        foreign_keys="Course.instructor_id",
        lazy="dynamic",
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        foreign_keys="Enrollment.student_id",
    )

    lesson_progress = db.relationship(
        "LessonProgress",
        back_populates="student",
        foreign_keys="LessonProgress.student_id",
    )

    quiz_attempts = db.relationship(
        "QuizAttempt",
        back_populates="student",
        foreign_keys="QuizAttempt.student_id",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": isoformat_or_none(self.created_at),
            "updated_at": isoformat_or_none(self.updated_at),
        }
