from pgvector.sqlalchemy import Vector

from app.extensions import db
from app.models.base import TimestampMixin


class AIConversation(TimestampMixin, db.Model):
    __tablename__ = "ai_conversations"

    id = db.Column(db.BigInteger, primary_key=True)
    student_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    course_id = db.Column(
        db.BigInteger,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )


class AIMessage(db.Model):
    __tablename__ = "ai_messages"

    id = db.Column(db.BigInteger, primary_key=True)
    conversation_id = db.Column(
        db.BigInteger,
        db.ForeignKey("ai_conversations.id"),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )


class CourseChunk(db.Model):
    __tablename__ = "course_chunks"

    id = db.Column(db.BigInteger, primary_key=True)
    chunk_id = db.Column(db.String(120), nullable=False, unique=True, index=True)
    course_id = db.Column(
        db.BigInteger,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )
    module_id = db.Column(
        db.BigInteger,
        db.ForeignKey("modules.id"),
        nullable=False,
        index=True,
    )
    lesson_id = db.Column(
        db.BigInteger,
        db.ForeignKey("lessons.id"),
        nullable=False,
        index=True,
    )
    module_title = db.Column(db.String(200), nullable=False)
    lesson_title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_hash = db.Column(db.String(64), nullable=False)
    embedding = db.Column(Vector(), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )
