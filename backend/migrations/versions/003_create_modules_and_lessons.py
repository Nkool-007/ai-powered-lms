"""create modules and lessons

Revision ID: 003
Revises: 002
"""

from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "modules",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("course_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
            name="fk_modules_course_id_courses",
        ),
        sa.UniqueConstraint(
            "course_id",
            "position",
            name="uq_modules_course_position",
        ),
    )
    op.create_index("ix_modules_course_id", "modules", ["course_id"], unique=False)

    op.create_table(
        "lessons",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("module_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["modules.id"],
            name="fk_lessons_module_id_modules",
        ),
        sa.UniqueConstraint(
            "module_id",
            "position",
            name="uq_lessons_module_position",
        ),
    )
    op.create_index("ix_lessons_module_id", "lessons", ["module_id"], unique=False)


def downgrade():
    op.drop_index("ix_lessons_module_id", table_name="lessons")
    op.drop_table("lessons")
    op.drop_index("ix_modules_course_id", table_name="modules")
    op.drop_table("modules")
