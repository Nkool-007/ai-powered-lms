from app.extensions import db
from app.models.base import ID_TYPE, TimestampMixin
from app.utils.serialization import isoformat_or_none


class Quiz(TimestampMixin, db.Model):
    __tablename__ = "quizzes"

    id = db.Column(ID_TYPE, primary_key=True)
    course_id = db.Column(
        ID_TYPE,
        db.ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    course = db.relationship("Course", back_populates="quizzes")

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

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "created_at": isoformat_or_none(self.created_at),
            "updated_at": isoformat_or_none(self.updated_at),
        }


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(ID_TYPE, primary_key=True)
    quiz_id = db.Column(
        ID_TYPE,
        db.ForeignKey("quizzes.id"),
        nullable=False,
        index=True,
    )
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False, default="MCQ")
    position = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "quiz_id",
            "position",
            name="uq_questions_quiz_position",
        ),
        db.CheckConstraint(
            "question_type = 'MCQ'",
            name="ck_questions_type",
        ),
        db.CheckConstraint(
            "position > 0",
            name="ck_questions_position_positive",
        ),
    )

    quiz = db.relationship("Quiz", back_populates="questions")

    options = db.relationship(
        "AnswerOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="AnswerOption.position",
    )

    student_answers = db.relationship(
        "StudentAnswer",
        back_populates="question",
    )


class AnswerOption(db.Model):
    __tablename__ = "answer_options"

    id = db.Column(ID_TYPE, primary_key=True)
    question_id = db.Column(
        ID_TYPE,
        db.ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    position = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "question_id",
            "position",
            name="uq_answer_options_question_position",
        ),
        db.CheckConstraint(
            "position > 0",
            name="ck_answer_options_position_positive",
        ),
    )

    question = db.relationship("Question", back_populates="options")

    selected_answers = db.relationship(
        "StudentAnswer",
        back_populates="selected_option",
    )


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(ID_TYPE, primary_key=True)
    quiz_id = db.Column(
        ID_TYPE,
        db.ForeignKey("quizzes.id"),
        nullable=False,
        index=True,
    )
    student_id = db.Column(
        ID_TYPE,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    score = db.Column(db.Numeric(5, 2), nullable=False)
    started_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )
    submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    quiz = db.relationship("Quiz", back_populates="attempts")

    student = db.relationship(
        "User",
        back_populates="quiz_attempts",
        foreign_keys=[student_id],
    )

    answers = db.relationship(
        "StudentAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "student_id": self.student_id,
            "score": float(self.score),
            "started_at": isoformat_or_none(self.started_at),
            "submitted_at": isoformat_or_none(self.submitted_at),
        }


class StudentAnswer(db.Model):
    __tablename__ = "student_answers"

    id = db.Column(ID_TYPE, primary_key=True)
    quiz_attempt_id = db.Column(
        ID_TYPE,
        db.ForeignKey("quiz_attempts.id"),
        nullable=False,
        index=True,
    )
    question_id = db.Column(
        ID_TYPE,
        db.ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )
    selected_option_id = db.Column(
        ID_TYPE,
        db.ForeignKey("answer_options.id"),
        nullable=False,
        index=True,
    )
    is_correct = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "quiz_attempt_id",
            "question_id",
            name="uq_student_answers_attempt_question",
        ),
    )

    attempt = db.relationship("QuizAttempt", back_populates="answers")
    question = db.relationship("Question", back_populates="student_answers")
    selected_option = db.relationship(
        "AnswerOption",
        back_populates="selected_answers",
    )
