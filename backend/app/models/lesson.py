from app.extensions import db
from app.models.base import BIGINT, TimestampMixin


class Lesson(TimestampMixin, db.Model):
    __tablename__ = "lessons"

    id = db.Column(BIGINT, primary_key=True)

    module_id = db.Column(
        BIGINT,
        db.ForeignKey("modules.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    position = db.Column(
        db.Integer,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "module_id",
            "position",
            name="uq_lessons_module_position",
        ),
    )

    module = db.relationship(
        "Module",
        back_populates="lessons",
    )

    progress_records = db.relationship(
        "LessonProgress",
        back_populates="lesson",
    )

    def to_dict(self, include_content=True):
        data = {
            "id": self.id,
            "module_id": self.module_id,
            "title": self.title,
            "position": self.position,
        }

        if include_content:
            data["content"] = self.content

        return data
