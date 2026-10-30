import json

from types import SimpleNamespace
from unittest.mock import patch

from app.ai.services.quiz_generator import QuizGeneratorService


def test_quiz_generator_uses_mocked_provider():
    raw_response = json.dumps(
        {
            "questions": [
                {
                    "question": "What is the purpose of a Python function?",
                    "options": [
                        "Store files",
                        "Group reusable instructions",
                        "Create databases",
                        "Start Docker",
                    ],
                    "correct_answer": 1,
                    "explanation": "A function groups reusable instructions.",
                }
            ]
        }
    )

    lesson = SimpleNamespace(
        id=42,
        title="Python Functions",
        content=(
            "A function groups reusable instructions under a name."
        ),
        module=SimpleNamespace(
            course_id=8,
        ),
    )

    user = SimpleNamespace(
        id=7,
    )

    with patch(
        "app.ai.services.quiz_generator.LLMService"
    ) as llm_service:
        llm_service.return_value.generate_text.return_value = raw_response

        draft = QuizGeneratorService().generate(
            lesson=lesson,
            difficulty="medium",
            number_of_questions=1,
            current_user=user,
        )

    assert draft["course_id"] == 8
    assert draft["lesson_id"] == 42
    assert len(draft["questions"]) == 1
    assert draft["questions"][0]["correct_answer"] == 1

    llm_service.return_value.generate_text.assert_called_once()
