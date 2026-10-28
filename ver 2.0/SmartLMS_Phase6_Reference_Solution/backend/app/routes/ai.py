from flask import Blueprint, request

from app.extensions import db
from app.models import AIConversation, AIMessage, Course, Enrollment, Lesson
from app.services.authorization import is_course_owner, roles_required
from app.utils.responses import error, success

from app.ai.exceptions import AIError
from app.ai.retriever.indexer import index_course
from app.ai.services.quiz_generator import QuizGeneratorService
from app.ai.services.tutor_service import TutorService


ai_bp = Blueprint("ai", __name__, url_prefix="/api/v1/ai")


def handle_ai_error(exc):
    from app.ai.exceptions import (
        AIConfigurationError,
        AIInvalidResponseError,
        AIProviderError,
        AIRateLimitError,
        AIRequestTimeoutError,
    )

    if isinstance(exc, AIConfigurationError):
        return error(
            "AI_CONFIGURATION_ERROR",
            "The AI service is not configured correctly.",
            503,
        )

    if isinstance(exc, AIRateLimitError):
        return error(
            "AI_RATE_LIMITED",
            "The AI service is temporarily busy. Please try again shortly.",
            429,
        )

    if isinstance(exc, AIRequestTimeoutError):
        return error("AI_REQUEST_TIMEOUT", "The AI request took too long.", 504)

    if isinstance(exc, AIInvalidResponseError):
        return error(
            "AI_INVALID_RESPONSE",
            "The AI service returned an invalid response.",
            502,
        )

    if isinstance(exc, AIProviderError):
        return error(
            "AI_SERVICE_UNAVAILABLE",
            "The AI service is temporarily unavailable.",
            503,
        )

    raise exc


@ai_bp.post("/generate-quiz")
@roles_required("INSTRUCTOR")
def generate_quiz(current_user):
    payload = request.get_json(silent=True) or {}

    lesson_id = payload.get("lesson_id")
    difficulty = str(payload.get("difficulty", "medium")).lower()
    number_of_questions = payload.get("number_of_questions", 5)

    if not isinstance(lesson_id, int):
        return error("VALIDATION_ERROR", "lesson_id is required.", 400)

    if difficulty not in {"easy", "medium", "hard"}:
        return error(
            "VALIDATION_ERROR",
            "difficulty must be easy, medium or hard.",
            400,
        )

    if not isinstance(number_of_questions, int) or not 1 <= number_of_questions <= 10:
        return error(
            "VALIDATION_ERROR",
            "number_of_questions must be between 1 and 10.",
            400,
        )

    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        return error("LESSON_NOT_FOUND", "Lesson does not exist.", 404)

    course = lesson.module.course
    if not is_course_owner(current_user, course):
        return error(
            "NOT_COURSE_OWNER",
            "You cannot generate a Quiz for this Lesson.",
            403,
        )

    try:
        draft = QuizGeneratorService().generate(
            lesson=lesson,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
            current_user=current_user,
        )
        return success(draft)
    except AIError as exc:
        return handle_ai_error(exc)


@ai_bp.post("/courses/<int:course_id>/reindex")
@roles_required("INSTRUCTOR")
def reindex_course(course_id, current_user):
    course = db.session.get(Course, course_id)
    if not course:
        return error("COURSE_NOT_FOUND", "Course does not exist.", 404)

    if not is_course_owner(current_user, course):
        return error("NOT_COURSE_OWNER", "You cannot index this Course.", 403)

    if course.status != "PUBLISHED":
        return error(
            "COURSE_NOT_PUBLISHED",
            "Publish the Course before building its AI index.",
            409,
        )

    try:
        return success(index_course(course))
    except AIError as exc:
        return handle_ai_error(exc)


@ai_bp.post("/chat")
@roles_required("STUDENT")
def chat(current_user):
    payload = request.get_json(silent=True) or {}

    course_id = payload.get("course_id")
    message = payload.get("message")
    conversation_id = payload.get("conversation_id")

    if not isinstance(course_id, int):
        return error("VALIDATION_ERROR", "course_id is required.", 400)

    if not isinstance(message, str) or not message.strip():
        return error("VALIDATION_ERROR", "message is required.", 400)

    course = db.session.get(Course, course_id)
    if not course:
        return error("COURSE_NOT_FOUND", "Course does not exist.", 404)

    enrollment = (
        Enrollment.query
        .filter_by(
            student_id=current_user.id,
            course_id=course.id,
            status="ACTIVE",
        )
        .first()
    )

    if not enrollment:
        return error(
            "COURSE_ENROLLMENT_REQUIRED",
            "You must be enrolled in this Course to use its Tutor.",
            403,
        )

    if conversation_id is not None:
        conversation = db.session.get(AIConversation, conversation_id)
        if (
            not conversation
            or conversation.student_id != current_user.id
            or conversation.course_id != course.id
        ):
            return error(
                "AI_CONVERSATION_NOT_FOUND",
                "Conversation does not exist.",
                404,
            )

    try:
        result = TutorService().ask(
            student=current_user,
            course=course,
            question=message.strip(),
            conversation_id=conversation_id,
        )
        return success(result)
    except AIError as exc:
        return handle_ai_error(exc)


@ai_bp.get("/conversations")
@roles_required("STUDENT")
def conversations(current_user):
    course_id = request.args.get("course_id", type=int)
    query = AIConversation.query.filter_by(student_id=current_user.id)

    if course_id is not None:
        query = query.filter_by(course_id=course_id)

    rows = query.order_by(AIConversation.updated_at.desc()).all()

    return success([
        {
            "id": row.id,
            "course_id": row.course_id,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
        }
        for row in rows
    ])


@ai_bp.get("/conversations/<int:conversation_id>")
@roles_required("STUDENT")
def conversation_detail(conversation_id, current_user):
    conversation = db.session.get(AIConversation, conversation_id)

    if not conversation or conversation.student_id != current_user.id:
        return error(
            "AI_CONVERSATION_NOT_FOUND",
            "Conversation does not exist.",
            404,
        )

    messages = (
        AIMessage.query
        .filter_by(conversation_id=conversation.id)
        .order_by(AIMessage.created_at.asc())
        .all()
    )

    return success({
        "id": conversation.id,
        "course_id": conversation.course_id,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            for message in messages
        ],
    })
