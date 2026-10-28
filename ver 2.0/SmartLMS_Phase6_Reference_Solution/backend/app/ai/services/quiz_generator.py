from pydantic import ValidationError

from app.ai.exceptions import AIInvalidResponseError
from app.ai.prompts.quiz_prompt import QUIZ_SYSTEM_PROMPT, build_quiz_prompt
from app.ai.schemas import GeneratedQuiz
from app.ai.services.llm_service import LLMService


class QuizGeneratorService:
    def generate(self, *, lesson, difficulty, number_of_questions, current_user):
        prompt = build_quiz_prompt(
            lesson_title=lesson.title,
            lesson_content=lesson.content,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
        )

        raw = LLMService().generate_text(
            system_prompt=QUIZ_SYSTEM_PROMPT,
            user_prompt=prompt,
            feature="quiz_generator",
            user_id=current_user.id,
            course_id=lesson.module.course_id,
        )

        try:
            quiz = GeneratedQuiz.model_validate_json(raw)
        except ValidationError as exc:
            raise AIInvalidResponseError("AI returned an invalid quiz structure.") from exc

        if len(quiz.questions) != number_of_questions:
            raise AIInvalidResponseError("AI returned an unexpected number of questions.")

        return {
            "course_id": lesson.module.course_id,
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "difficulty": difficulty,
            "questions": [question.model_dump() for question in quiz.questions],
        }
