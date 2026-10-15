from app.extensions import db
from app.models.base import BIGINT


class LessonProgress(db.Model):
    __tablename__ = "lesson_progress"

    id = db.Column(BIGINT, primary_key=True)

    student_id = db.Column(
        BIGINT,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    lesson_id = db.Column(
        BIGINT,
        db.ForeignKey("lessons.id"),
        nullable=False,
        index=True,
    )

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    last_accessed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "lesson_id",
            name="uq_progress_student_lesson",
        ),
    )

    student = db.relationship(
        "User",
        back_populates="lesson_progress",
    )

    lesson = db.relationship(
        "Lesson",
        back_populates="progress_records",
    )
