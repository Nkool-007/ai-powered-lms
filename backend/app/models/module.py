from app.extensions import db
from app.models.base import BIGINT, TimestampMixin


class Module(TimestampMixin, db.Model):
    __tablename__ = "modules"

    id = db.Column(BIGINT, primary_key=True)

    course_id = db.Column(
        BIGINT,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    position = db.Column(
        db.Integer,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "course_id",
            "position",
            name="uq_modules_course_position",
        ),
    )

    course = db.relationship(
        "Course",
        back_populates="modules",
    )

    lessons = db.relationship(
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.position",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "position": self.position,
        }
