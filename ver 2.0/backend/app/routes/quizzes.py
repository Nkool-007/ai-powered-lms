from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import (
    AnswerOption,
    Course,
    Enrollment,
    Question,
    Quiz,
    QuizAttempt,
    StudentAnswer,
)
from app.services.authorization import (
    get_current_user,
    is_course_owner,
    roles_required,
    student_has_course_access,
)
from app.utils.responses import error, success
from app.utils.serialization import isoformat_or_none
from app.utils.validators import positive_integer, required_string


quizzes_bp = Blueprint(
    "quizzes",
    __name__,
    url_prefix="/api/v1",
)


def student_quiz_dict(quiz):
    return {
        "id": quiz.id,
        "course_id": quiz.course_id,
        "title": quiz.title,
        "description": quiz.description,
        "questions": [
            {
                "id": question.id,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "position": question.position,
                "options": [
                    {
                        "id": option.id,
                        "option_text": option.option_text,
                        "position": option.position,
                    }
                    for option in question.options
                ],
            }
            for question in quiz.questions
        ],
    }


def instructor_quiz_dict(quiz):
    return {
        "id": quiz.id,
        "course_id": quiz.course_id,
        "title": quiz.title,
        "description": quiz.description,
        "questions": [
            {
                "id": question.id,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "position": question.position,
                "options": [
                    {
                        "id": option.id,
                        "option_text": option.option_text,
                        "position": option.position,
                        "is_correct": option.is_correct,
                    }
                    for option in question.options
                ],
            }
            for question in quiz.questions
        ],
    }


def _validate_quiz_payload(payload):
    title = payload.get("title")
    questions = payload.get("questions")

    if not required_string(title):
        return "Quiz title is required."

    if not isinstance(questions, list) or not questions:
        return "Quiz must contain at least one question."

    question_positions = set()

    for question in questions:
        if not isinstance(question, dict):
            return "Each question must be an object."

        if not required_string(question.get("question_text")):
            return "Every question requires question_text."

        position = question.get("position")

        if not positive_integer(position):
            return "Every question requires a positive integer position."

        if position in question_positions:
            return "Question positions must be unique within a quiz."

        question_positions.add(position)

        options = question.get("options")

        if not isinstance(options, list) or len(options) < 2:
            return "Every MCQ requires at least two options."

        option_positions = set()
        correct_count = 0

        for option in options:
            if not isinstance(option, dict):
                return "Each answer option must be an object."

            if not required_string(option.get("option_text")):
                return "Every answer option requires option_text."

            option_position = option.get("position")

            if not positive_integer(option_position):
                return "Every option requires a positive integer position."

            if option_position in option_positions:
                return "Option positions must be unique within each question."

            option_positions.add(option_position)

            if option.get("is_correct") is True:
                correct_count += 1

        if correct_count != 1:
            return "Every MCQ must have exactly one correct option."

    return None


@quizzes_bp.post("/courses/<int:course_id>/quizzes")
@roles_required("INSTRUCTOR")
def create_quiz(course_id, current_user):
    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if not is_course_owner(current_user, course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot modify another instructor's course.",
            403,
        )

    payload = request.get_json(silent=True) or {}
    validation_error = _validate_quiz_payload(payload)

    if validation_error:
        return error(
            "VALIDATION_ERROR",
            validation_error,
            400,
        )

    quiz = Quiz(
        course_id=course.id,
        title=payload["title"].strip(),
        description=(
            payload.get("description", "").strip()
            if isinstance(payload.get("description"), str)
            else None
        ),
    )

    db.session.add(quiz)

    try:
        db.session.flush()

        for question_payload in payload["questions"]:
            question = Question(
                quiz_id=quiz.id,
                question_text=question_payload["question_text"].strip(),
                question_type="MCQ",
                position=question_payload["position"],
            )

            db.session.add(question)
            db.session.flush()

            for option_payload in question_payload["options"]:
                db.session.add(
                    AnswerOption(
                        question_id=question.id,
                        option_text=option_payload["option_text"].strip(),
                        is_correct=bool(option_payload.get("is_correct", False)),
                        position=option_payload["position"],
                    )
                )

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return success(
        instructor_quiz_dict(quiz),
        201,
    )


@quizzes_bp.get("/courses/<int:course_id>/quizzes")
@jwt_required()
def list_course_quizzes(course_id):
    user = get_current_user()

    if not user:
        return error(
            "AUTHENTICATION_REQUIRED",
            "Authentication is required.",
            401,
        )

    if not user.is_active:
        return error(
            "ACCOUNT_DISABLED",
            "This account has been disabled.",
            403,
        )

    course = db.session.get(Course, course_id)

    if not course:
        return error(
            "COURSE_NOT_FOUND",
            "Course does not exist.",
            404,
        )

    if user.role == "STUDENT":
        if not student_has_course_access(user.id, course.id):
            return error(
                "COURSE_ENROLLMENT_REQUIRED",
                "You must be enrolled in this course.",
                403,
            )

    elif user.role == "INSTRUCTOR":
        if not is_course_owner(user, course):
            return error(
                "NOT_COURSE_OWNER",
                "You cannot view quizzes for this course.",
                403,
            )

    elif user.role != "ADMIN":
        return error(
            "INSUFFICIENT_PERMISSION",
            "You do not have permission to view these quizzes.",
            403,
        )

    quizzes = (
        Quiz.query
        .filter_by(course_id=course.id)
        .order_by(Quiz.created_at.asc())
        .all()
    )

    return success([
        quiz.to_dict()
        for quiz in quizzes
    ])


@quizzes_bp.get("/quizzes/<int:quiz_id>")
@jwt_required()
def get_quiz(quiz_id):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return error(
            "QUIZ_NOT_FOUND",
            "Quiz does not exist.",
            404,
        )

    user = get_current_user()

    if not user:
        return error(
            "AUTHENTICATION_REQUIRED",
            "Authentication is required.",
            401,
        )

    if not user.is_active:
        return error(
            "ACCOUNT_DISABLED",
            "This account has been disabled.",
            403,
        )

    if user.role == "STUDENT":
        if not student_has_course_access(
            user.id,
            quiz.course_id,
        ):
            return error(
                "COURSE_ENROLLMENT_REQUIRED",
                "You must be enrolled in this course.",
                403,
            )

        return success(student_quiz_dict(quiz))

    if user.role == "INSTRUCTOR":
        if not is_course_owner(user, quiz.course):
            return error(
                "NOT_COURSE_OWNER",
                "You cannot access another instructor's quiz.",
                403,
            )

        return success(instructor_quiz_dict(quiz))

    if user.role == "ADMIN":
        return success(instructor_quiz_dict(quiz))

    return error(
        "INSUFFICIENT_PERMISSION",
        "You do not have permission to access this quiz.",
        403,
    )


@quizzes_bp.post("/quizzes/<int:quiz_id>/submit")
@roles_required("STUDENT")
def submit_quiz(quiz_id, current_user):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return error(
            "QUIZ_NOT_FOUND",
            "Quiz does not exist.",
            404,
        )

    if not student_has_course_access(
        current_user.id,
        quiz.course_id,
    ):
        return error(
            "COURSE_ENROLLMENT_REQUIRED",
            "You must be enrolled in this course.",
            403,
        )

    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers")

    if not isinstance(answers, list):
        return error(
            "INVALID_QUIZ_SUBMISSION",
            "answers must be an array.",
            400,
        )

    questions = {
        question.id: question
        for question in quiz.questions
    }

    if not questions:
        return error(
            "INVALID_QUIZ_SUBMISSION",
            "Quiz contains no questions.",
            400,
        )

    if len(answers) != len(questions):
        return error(
            "INVALID_QUIZ_SUBMISSION",
            "Every quiz question must be answered exactly once.",
            400,
        )

    seen_question_ids = set()
    validated_answers = []

    for answer in answers:
        if not isinstance(answer, dict):
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Every answer must be an object.",
                400,
            )

        question_id = answer.get("question_id")
        selected_option_id = answer.get("selected_option_id")

        try:
            question_id = int(question_id)
            selected_option_id = int(selected_option_id)
        except (TypeError, ValueError):
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Question and option IDs must be integers.",
                400,
            )

        if question_id in seen_question_ids:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "A question cannot be answered more than once.",
                400,
            )

        question = questions.get(question_id)

        if not question:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Question does not belong to this quiz.",
                400,
            )

        option = next(
            (
                candidate
                for candidate in question.options
                if candidate.id == selected_option_id
            ),
            None,
        )

        if not option:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Selected option does not belong to the question.",
                400,
            )

        seen_question_ids.add(question_id)

        validated_answers.append(
            (question, option)
        )

    correct_answers = sum(
        1
        for _, option in validated_answers
        if option.is_correct
    )

    score = round(
        (correct_answers / len(questions)) * 100,
        2,
    )

    now = datetime.now(timezone.utc)

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        student_id=current_user.id,
        score=score,
        submitted_at=now,
    )

    db.session.add(attempt)

    try:
        db.session.flush()

        for question, option in validated_answers:
            db.session.add(
                StudentAnswer(
                    quiz_attempt_id=attempt.id,
                    question_id=question.id,
                    selected_option_id=option.id,
                    is_correct=option.is_correct,
                )
            )

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return success({
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "score": float(score),
        "total_questions": len(questions),
        "correct_answers": correct_answers,
        "submitted_at": isoformat_or_none(attempt.submitted_at),
    }, 201)


@quizzes_bp.get("/students/me/quiz-attempts")
@roles_required("STUDENT")
def my_quiz_attempts(current_user):
    course_id = request.args.get(
        "course_id",
        type=int,
    )

    query = (
        QuizAttempt.query
        .join(Quiz)
        .filter(
            QuizAttempt.student_id == current_user.id
        )
    )

    if course_id is not None:
        query = query.filter(
            Quiz.course_id == course_id
        )

    attempts = (
        query
        .order_by(QuizAttempt.submitted_at.desc())
        .all()
    )

    return success([
        {
            "attempt_id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "quiz_title": attempt.quiz.title,
            "course_id": attempt.quiz.course_id,
            "score": float(attempt.score),
            "total_questions": len(attempt.quiz.questions),
            "submitted_at": isoformat_or_none(attempt.submitted_at),
        }
        for attempt in attempts
    ])
