"""create quiz attempts and student answers

Revision ID: 007
Revises: 006
"""
from alembic import op
import sqlalchemy as sa

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "quiz_attempts",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("quiz_id", sa.BigInteger(), nullable=False),
        sa.Column("student_id", sa.BigInteger(), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["quiz_id"], ["quizzes.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
    )
    op.create_index("ix_quiz_attempts_quiz_id", "quiz_attempts", ["quiz_id"])
    op.create_index("ix_quiz_attempts_student_id", "quiz_attempts", ["student_id"])

    op.create_table(
        "student_answers",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("quiz_attempt_id", sa.BigInteger(), nullable=False),
        sa.Column("question_id", sa.BigInteger(), nullable=False),
        sa.Column("selected_option_id", sa.BigInteger(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["quiz_attempt_id"], ["quiz_attempts.id"]),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.ForeignKeyConstraint(["selected_option_id"], ["answer_options.id"]),
        sa.UniqueConstraint(
            "quiz_attempt_id",
            "question_id",
            name="uq_student_answers_attempt_question",
        ),
    )
    op.create_index("ix_student_answers_attempt_id", "student_answers", ["quiz_attempt_id"])
    op.create_index("ix_student_answers_question_id", "student_answers", ["question_id"])
    op.create_index("ix_student_answers_selected_option_id", "student_answers", ["selected_option_id"])


def downgrade():
    op.drop_index("ix_student_answers_selected_option_id", table_name="student_answers")
    op.drop_index("ix_student_answers_question_id", table_name="student_answers")
    op.drop_index("ix_student_answers_attempt_id", table_name="student_answers")
    op.drop_table("student_answers")
    op.drop_index("ix_quiz_attempts_student_id", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_quiz_id", table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
