"""Phase 6: enable pgvector and create course_chunks.

Reference revision IDs follow the conceptual Phase 6 migration sequence in the solution.
If your existing Alembic repository uses generated revision hashes, replace revision/down_revision
with values matching your actual migration history before applying this file.
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "course_chunks",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("chunk_id", sa.String(length=120), nullable=False),
        sa.Column("course_id", sa.BigInteger(), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("module_id", sa.BigInteger(), sa.ForeignKey("modules.id"), nullable=False),
        sa.Column("lesson_id", sa.BigInteger(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("module_title", sa.String(length=200), nullable=False),
        sa.Column("lesson_title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("embedding", Vector(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("chunk_id"),
    )

    op.create_index("ix_course_chunks_course_id", "course_chunks", ["course_id"])


def downgrade():
    op.drop_table("course_chunks")
