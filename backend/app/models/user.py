from app.extensions import db
from app.models.base import BIGINT, TimestampMixin


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(BIGINT, primary_key=True)

    name = db.Column(
        db.String(120),
        nullable=False,
    )

    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    role = db.Column(
        db.String(20),
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    __table_args__ = (
        db.CheckConstraint(
            "role IN ('STUDENT', 'INSTRUCTOR', 'ADMIN')",
            name="ck_users_role",
        ),
    )

    courses_created = db.relationship(
        "Course",
        back_populates="instructor",
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
    )

    lesson_progress = db.relationship(
        "LessonProgress",
        back_populates="student",
    )

    quiz_attempts = db.relationship(
        "QuizAttempt",
        back_populates="student",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
