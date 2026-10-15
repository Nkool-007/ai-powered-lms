from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

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
from app.services.authorization import is_course_owner, roles_required
from app.utils.responses import error, success
from app.utils.validators import required_string

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
                "question": question.question_text,
                "type": question.question_type,
                "position": question.position,
                "options": [
                    {
                        "id": option.id,
                        "text": option.option_text,
                        "position": option.position,
                    }
                    for option in question.options
                ],
            }
            for question in quiz.questions
        ],
    }


def instructor_quiz_dict(quiz):
    result = student_quiz_dict(quiz)

    for question_data, question in zip(
        result["questions"],
        quiz.questions,
    ):
        for option_data, option in zip(
            question_data["options"],
            question.options,
        ):
            option_data["is_correct"] = option.is_correct

    return result


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
            "You cannot create quizzes for another instructor's course.",
            403,
        )

    payload = request.get_json(silent=True) or {}

    title = payload.get("title")
    description = payload.get("description")
    questions_data = payload.get("questions", [])

    if not required_string(title):
        return error(
            "VALIDATION_ERROR",
            "Quiz title is required.",
            400,
        )

    if not isinstance(questions_data, list) or not questions_data:
        return error(
            "VALIDATION_ERROR",
            "Quiz must contain at least one question.",
            400,
        )

    quiz = Quiz(
        course_id=course.id,
        title=title.strip(),
        description=(
            description.strip()
            if isinstance(description, str)
            else None
        ),
    )

    db.session.add(quiz)

    try:
        for q_index, q_data in enumerate(
            questions_data,
            start=1,
        ):
            question_text = q_data.get("question_text")
            position = q_data.get("position", q_index)
            options_data = q_data.get("options", [])

            if not required_string(question_text):
                raise ValueError(
                    "Every question requires question_text."
                )

            if not isinstance(options_data, list) or len(options_data) < 2:
                raise ValueError(
                    "Every question requires at least two options."
                )

            correct_count = sum(
                1
                for option in options_data
                if option.get("is_correct") is True
            )

            if correct_count != 1:
                raise ValueError(
                    "Each MCQ must contain exactly one correct option."
                )

            question = Question(
                quiz=quiz,
                question_text=question_text.strip(),
                question_type="MCQ",
                position=position,
            )

            db.session.add(question)

            for o_index, option_data in enumerate(
                options_data,
                start=1,
            ):
                option_text = option_data.get("option_text")

                if not required_string(option_text):
                    raise ValueError(
                        "Every option requires option_text."
                    )

                option = AnswerOption(
                    question=question,
                    option_text=option_text.strip(),
                    is_correct=bool(
                        option_data.get("is_correct", False)
                    ),
                    position=option_data.get("position", o_index),
                )

                db.session.add(option)

        db.session.commit()

    except ValueError as exc:
        db.session.rollback()
        return error(
            "VALIDATION_ERROR",
            str(exc),
            400,
        )

    except IntegrityError:
        db.session.rollback()
        return error(
            "QUIZ_STRUCTURE_CONFLICT",
            "Quiz question or option positions conflict.",
            409,
        )

    return success(
        instructor_quiz_dict(quiz),
        201,
    )


@quizzes_bp.get("/quizzes/<int:quiz_id>")
@roles_required(
    "STUDENT",
    "INSTRUCTOR",
    "ADMIN",
)
def get_quiz(quiz_id, current_user):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return error(
            "QUIZ_NOT_FOUND",
            "Quiz does not exist.",
            404,
        )

    if current_user.role == "STUDENT":
        enrollment = (
            Enrollment.query
            .filter_by(
                student_id=current_user.id,
                course_id=quiz.course_id,
            )
            .first()
        )

        if not enrollment:
            return error(
                "COURSE_ENROLLMENT_REQUIRED",
                "You must be enrolled to attempt this quiz.",
                403,
            )

        return success(student_quiz_dict(quiz))

    if current_user.role == "INSTRUCTOR":
        if not is_course_owner(current_user, quiz.course):
            return error(
                "NOT_COURSE_OWNER",
                "You cannot access this instructor quiz.",
                403,
            )

    return success(instructor_quiz_dict(quiz))


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

    enrollment = (
        Enrollment.query
        .filter_by(
            student_id=current_user.id,
            course_id=quiz.course_id,
        )
        .first()
    )

    if not enrollment:
        return error(
            "COURSE_ENROLLMENT_REQUIRED",
            "You must be enrolled to attempt this quiz.",
            403,
        )

    payload = request.get_json(silent=True) or {}
    submitted_answers = payload.get("answers")

    if not isinstance(submitted_answers, list):
        return error(
            "INVALID_QUIZ_SUBMISSION",
            "answers must be an array.",
            400,
        )

    quiz_questions = {
        question.id: question
        for question in quiz.questions
    }

    if len(submitted_answers) != len(quiz_questions):
        return error(
            "INVALID_QUIZ_SUBMISSION",
            "Every quiz question must be answered exactly once.",
            400,
        )

    seen_questions = set()
    validated_answers = []

    for submitted in submitted_answers:
        question_id = submitted.get("question_id")
        option_id = submitted.get("selected_option_id")

        if question_id in seen_questions:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "A question cannot be answered more than once.",
                400,
            )

        question = quiz_questions.get(question_id)

        if not question:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Submitted question does not belong to this quiz.",
                400,
            )

        option = db.session.get(AnswerOption, option_id)

        if not option or option.question_id != question.id:
            return error(
                "INVALID_QUIZ_SUBMISSION",
                "Selected option does not belong to the submitted question.",
                400,
            )

        seen_questions.add(question_id)
        validated_answers.append((question, option))

    correct_answers = sum(
        1
        for _, option in validated_answers
        if option.is_correct
    )

    total_questions = len(quiz_questions)

    score = round(
        (correct_answers / total_questions) * 100,
        2,
    )

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        student_id=current_user.id,
        score=score,
    )

    db.session.add(attempt)
    db.session.flush()

    for question, option in validated_answers:
        answer = StudentAnswer(
            quiz_attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=option.id,
            is_correct=option.is_correct,
        )
        db.session.add(answer)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return success(
        {
            "attempt_id": attempt.id,
            "score": float(attempt.score),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
        },
        201,
    )


@quizzes_bp.get("/students/me/quiz-attempts")
@roles_required("STUDENT")
def my_quiz_attempts(current_user):
    course_id = request.args.get(
        "course_id",
        type=int,
    )

    query = (
        QuizAttempt.query
        .filter_by(student_id=current_user.id)
        .join(Quiz)
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

    return success(
        [
            {
                "attempt_id": attempt.id,
                "quiz_id": attempt.quiz_id,
                "quiz_title": attempt.quiz.title,
                "course_id": attempt.quiz.course_id,
                "score": float(attempt.score),
                "submitted_at": attempt.submitted_at.isoformat(),
            }
            for attempt in attempts
        ]
    )
