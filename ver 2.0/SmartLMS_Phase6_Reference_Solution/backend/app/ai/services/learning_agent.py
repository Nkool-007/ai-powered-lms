import json

from app.ai.agents.tools import (
    get_course_structure,
    get_quiz_performance,
    get_student_progress,
    search_course_content,
)
from app.ai.services.llm_service import LLMService


AGENT_SYSTEM_PROMPT = """
You are the SmartLMS Learning Agent.

Use the supplied authenticated LMS state to recommend a useful next learning activity.

Do not invent progress, Quiz scores, Course structure, or Lesson names.

Keep the recommendation concise and actionable.
"""


class LearningAgentService:
    def recommend(self, *, student, course):
        progress = get_student_progress(student_id=student.id, course_id=course.id)
        quiz_performance = get_quiz_performance(student_id=student.id, course_id=course.id)
        structure = get_course_structure(student_id=student.id, course_id=course.id)
        relevant_content = search_course_content(
            student_id=student.id,
            course_id=course.id,
            query="important concepts for the student's next study activity",
        )

        state = {
            "progress": progress,
            "quiz_performance": quiz_performance,
            "course_structure": structure,
            "relevant_content": relevant_content,
        }

        answer = LLMService().generate_text(
            system_prompt=AGENT_SYSTEM_PROMPT,
            user_prompt=(
                "Authenticated LMS state:\n\n"
                + json.dumps(state, default=str)
                + "\n\nRecommend what the Student should study next."
            ),
            feature="learning_agent",
            user_id=student.id,
            course_id=course.id,
        )

        return {
            "recommendation": answer,
            "state_used": {
                "progress": True,
                "quiz_performance": True,
                "course_structure": True,
                "course_content": True,
            },
        }
