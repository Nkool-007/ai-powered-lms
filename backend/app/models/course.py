from app.extensions import db
from app.models.base import BIGINT, TimestampMixin


class Course(TimestampMixin, db.Model):
    __tablename__ = "courses"

    id = db.Column(BIGINT, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    instructor_id = db.Column(
        BIGINT,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="DRAFT",
    )

    published_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('DRAFT', 'PUBLISHED')",
            name="ck_courses_status",
        ),
    )

    instructor = db.relationship(
        "User",
        back_populates="courses_created",
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
            "status": self.status,
            "instructor_id": self.instructor_id,
            "published_at": (
                self.published_at.isoformat() if self.published_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_instructor and self.instructor:
            data["instructor"] = {
                "id": self.instructor.id,
                "name": self.instructor.name,
            }

        return data
