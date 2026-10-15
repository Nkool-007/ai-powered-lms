from app.extensions import db
from app.models.base import BIGINT, TimestampMixin


class Quiz(TimestampMixin, db.Model):
    __tablename__ = "quizzes"

    id = db.Column(BIGINT, primary_key=True)

    course_id = db.Column(
        BIGINT,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    course = db.relationship(
        "Course",
        back_populates="quizzes",
    )

    questions = db.relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.position",
    )

    attempts = db.relationship(
        "QuizAttempt",
        back_populates="quiz",
    )


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(BIGINT, primary_key=True)

    quiz_id = db.Column(
        BIGINT,
        db.ForeignKey("quizzes.id"),
        nullable=False,
        index=True,
    )

    question_text = db.Column(
        db.Text,
        nullable=False,
    )

    question_type = db.Column(
        db.String(20),
        nullable=False,
        default="MCQ",
    )

    position = db.Column(
        db.Integer,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "quiz_id",
            "position",
            name="uq_question_quiz_position",
        ),
    )

    quiz = db.relationship(
        "Quiz",
        back_populates="questions",
    )

    options = db.relationship(
        "AnswerOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="AnswerOption.position",
    )


class AnswerOption(db.Model):
    __tablename__ = "answer_options"

    id = db.Column(BIGINT, primary_key=True)

    question_id = db.Column(
        BIGINT,
        db.ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    option_text = db.Column(
        db.Text,
        nullable=False,
    )

    is_correct = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    position = db.Column(
        db.Integer,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "question_id",
            "position",
            name="uq_option_question_position",
        ),
    )

    question = db.relationship(
        "Question",
        back_populates="options",
    )


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(BIGINT, primary_key=True)

    quiz_id = db.Column(
        BIGINT,
        db.ForeignKey("quizzes.id"),
        nullable=False,
        index=True,
    )

    student_id = db.Column(
        BIGINT,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    score = db.Column(
        db.Numeric(5, 2),
        nullable=False,
    )

    started_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )

    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )

    quiz = db.relationship(
        "Quiz",
        back_populates="attempts",
    )

    student = db.relationship(
        "User",
        back_populates="quiz_attempts",
    )

    answers = db.relationship(
        "StudentAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class StudentAnswer(db.Model):
    __tablename__ = "student_answers"

    id = db.Column(BIGINT, primary_key=True)

    quiz_attempt_id = db.Column(
        BIGINT,
        db.ForeignKey("quiz_attempts.id"),
        nullable=False,
        index=True,
    )

    question_id = db.Column(
        BIGINT,
        db.ForeignKey("questions.id"),
        nullable=False,
    )

    selected_option_id = db.Column(
        BIGINT,
        db.ForeignKey("answer_options.id"),
        nullable=False,
    )

    is_correct = db.Column(
        db.Boolean,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "quiz_attempt_id",
            "question_id",
            name="uq_student_answer_attempt_question",
        ),
    )

    attempt = db.relationship(
        "QuizAttempt",
        back_populates="answers",
    )

    question = db.relationship("Question")
    selected_option = db.relationship("AnswerOption")
