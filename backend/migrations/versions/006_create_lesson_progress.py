"""create lesson progress

Revision ID: 006
Revises: 005
"""

from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("student_id", sa.BigInteger(), nullable=False),
        sa.Column("lesson_id", sa.BigInteger(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_lesson_progress_student_id_users",
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
            name="fk_lesson_progress_lesson_id_lessons",
        ),
        sa.UniqueConstraint(
            "student_id",
            "lesson_id",
            name="uq_progress_student_lesson",
        ),
    )
    op.create_index(
        "ix_lesson_progress_student_id",
        "lesson_progress",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "ix_lesson_progress_lesson_id",
        "lesson_progress",
        ["lesson_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_lesson_progress_lesson_id", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_student_id", table_name="lesson_progress")
    op.drop_table("lesson_progress")
