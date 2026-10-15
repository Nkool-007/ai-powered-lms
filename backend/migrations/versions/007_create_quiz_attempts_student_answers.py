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
        sa.Column("score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["quiz_id"],
            ["quizzes.id"],
            name="fk_quiz_attempts_quiz_id_quizzes",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_quiz_attempts_student_id_users",
        ),
    )
    op.create_index("ix_quiz_attempts_quiz_id", "quiz_attempts", ["quiz_id"], unique=False)
    op.create_index(
        "ix_quiz_attempts_student_id",
        "quiz_attempts",
        ["student_id"],
        unique=False,
    )

    op.create_table(
        "student_answers",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("quiz_attempt_id", sa.BigInteger(), nullable=False),
        sa.Column("question_id", sa.BigInteger(), nullable=False),
        sa.Column("selected_option_id", sa.BigInteger(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["quiz_attempt_id"],
            ["quiz_attempts.id"],
            name="fk_student_answers_quiz_attempt_id_quiz_attempts",
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name="fk_student_answers_question_id_questions",
        ),
        sa.ForeignKeyConstraint(
            ["selected_option_id"],
            ["answer_options.id"],
            name="fk_student_answers_selected_option_id_answer_options",
        ),
        sa.UniqueConstraint(
            "quiz_attempt_id",
            "question_id",
            name="uq_student_answer_attempt_question",
        ),
    )
    op.create_index(
        "ix_student_answers_quiz_attempt_id",
        "student_answers",
        ["quiz_attempt_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        "ix_student_answers_quiz_attempt_id",
        table_name="student_answers",
    )
    op.drop_table("student_answers")
    op.drop_index("ix_quiz_attempts_student_id", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_quiz_id", table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
