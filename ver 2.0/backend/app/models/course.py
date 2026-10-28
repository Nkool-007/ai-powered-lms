from app.extensions import db
from app.models.base import ID_TYPE, TimestampMixin
from app.utils.serialization import isoformat_or_none


class Course(TimestampMixin, db.Model):
    __tablename__ = "courses"

    id = db.Column(ID_TYPE, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(
        ID_TYPE,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    status = db.Column(db.String(20), nullable=False, default="DRAFT")
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('DRAFT', 'PUBLISHED')",
            name="ck_courses_status",
        ),
    )

    instructor = db.relationship(
        "User",
        back_populates="courses",
        foreign_keys=[instructor_id],
    )

    modules = db.relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.position",
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
    )

    quizzes = db.relationship(
        "Quiz",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_instructor=True):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "instructor_id": self.instructor_id,
            "status": self.status,
            "published_at": isoformat_or_none(self.published_at),
            "created_at": isoformat_or_none(self.created_at),
            "updated_at": isoformat_or_none(self.updated_at),
        }

        if include_instructor and self.instructor:
            data["instructor"] = {
                "id": self.instructor.id,
                "name": self.instructor.name,
            }

        return data
