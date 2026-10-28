"""create quizzes questions options

Revision ID: 005
Revises: 004
"""
from alembic import op
import sqlalchemy as sa

revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "quizzes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("course_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
    )
    op.create_index("ix_quizzes_course_id", "quizzes", ["course_id"])

    op.create_table(
        "questions",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("quiz_id", sa.BigInteger(), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(length=20), nullable=False, server_default="MCQ"),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["quiz_id"], ["quizzes.id"]),
        sa.UniqueConstraint(
            "quiz_id",
            "position",
            name="uq_questions_quiz_position",
        ),
        sa.CheckConstraint(
            "question_type = 'MCQ'",
            name="ck_questions_type",
        ),
        sa.CheckConstraint(
            "position > 0",
            name="ck_questions_position_positive",
        ),
    )
    op.create_index("ix_questions_quiz_id", "questions", ["quiz_id"])

    op.create_table(
        "answer_options",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("question_id", sa.BigInteger(), nullable=False),
        sa.Column("option_text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.UniqueConstraint(
            "question_id",
            "position",
            name="uq_answer_options_question_position",
        ),
        sa.CheckConstraint(
            "position > 0",
            name="ck_answer_options_position_positive",
        ),
    )
    op.create_index("ix_answer_options_question_id", "answer_options", ["question_id"])


def downgrade():
    op.drop_index("ix_answer_options_question_id", table_name="answer_options")
    op.drop_table("answer_options")
    op.drop_index("ix_questions_quiz_id", table_name="questions")
    op.drop_table("questions")
    op.drop_index("ix_quizzes_course_id", table_name="quizzes")
    op.drop_table("quizzes")
