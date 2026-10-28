QUIZ_SYSTEM_PROMPT = """
You are an educational quiz-generation assistant.

Generate multiple-choice questions using only the supplied Lesson content.

Requirements:
1. Return valid JSON only.
2. Do not include Markdown fences.
3. Every question must contain:
   - question
   - options
   - correct_answer
   - explanation
4. correct_answer must be the zero-based index of the correct option.
5. Every question must have exactly four options.
6. Exactly one option must be correct.
7. Questions must match the requested difficulty.
8. Do not introduce facts unsupported by the Lesson.
"""


def build_quiz_prompt(*, lesson_title, lesson_content, difficulty, number_of_questions):
    return f"""
LESSON TITLE:
{lesson_title}

LESSON CONTENT:
{lesson_content}

DIFFICULTY:
{difficulty}

NUMBER OF QUESTIONS:
{number_of_questions}

Return exactly this JSON structure:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": 0,
      "explanation": "..."
    }}
  ]
}}
"""
