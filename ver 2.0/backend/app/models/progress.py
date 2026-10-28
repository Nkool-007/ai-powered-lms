from app.extensions import db
from app.models.base import ID_TYPE
from app.utils.serialization import isoformat_or_none


class LessonProgress(db.Model):
    __tablename__ = "lesson_progress"

    id = db.Column(ID_TYPE, primary_key=True)
    student_id = db.Column(
        ID_TYPE,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    lesson_id = db.Column(
        ID_TYPE,
        db.ForeignKey("lessons.id"),
        nullable=False,
        index=True,
    )
    completed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_accessed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "lesson_id",
            name="uq_lesson_progress_student_lesson",
        ),
    )

    student = db.relationship(
        "User",
        back_populates="lesson_progress",
        foreign_keys=[student_id],
    )

    lesson = db.relationship(
        "Lesson",
        back_populates="progress_records",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "lesson_id": self.lesson_id,
            "completed": self.completed,
            "completed_at": isoformat_or_none(self.completed_at),
            "last_accessed_at": isoformat_or_none(self.last_accessed_at),
        }
