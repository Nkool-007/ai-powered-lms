"""create courses

Revision ID: 002
Revises: 001
"""

from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "courses",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("instructor_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="DRAFT"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "status IN ('DRAFT', 'PUBLISHED')",
            name="ck_courses_status",
        ),
        sa.ForeignKeyConstraint(
            ["instructor_id"],
            ["users.id"],
            name="fk_courses_instructor_id_users",
        ),
    )
    op.create_index("ix_courses_instructor_id", "courses", ["instructor_id"], unique=False)


def downgrade():
    op.drop_index("ix_courses_instructor_id", table_name="courses")
    op.drop_table("courses")
