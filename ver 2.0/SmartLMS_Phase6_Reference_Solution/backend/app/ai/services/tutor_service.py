from datetime import datetime, timezone

from app.extensions import db
from app.models import AIConversation, AIMessage
from app.ai.prompts.tutor_prompt import TUTOR_SYSTEM_PROMPT, build_tutor_prompt
from app.ai.retriever.course_retriever import CourseRetriever
from app.ai.services.llm_service import LLMService


INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not find enough relevant information in this Course material to answer confidently."
)


class TutorService:
    def _conversation(self, *, student_id, course_id, conversation_id=None):
        if conversation_id is None:
            return None

        conversation = db.session.get(AIConversation, conversation_id)
        if (
            not conversation
            or conversation.student_id != student_id
            or conversation.course_id != course_id
        ):
            return None
        return conversation

    def _history_text(self, conversation):
        if conversation is None:
            return ""

        messages = (
            AIMessage.query
            .filter_by(conversation_id=conversation.id)
            .order_by(AIMessage.created_at.desc())
            .limit(6)
            .all()
        )
        messages.reverse()
        return "\n".join(f"{message.role}: {message.content}" for message in messages)

    def _sources(self, chunks):
        seen = set()
        sources = []
        for chunk in chunks:
            lesson_id = chunk["lesson_id"]
            if lesson_id in seen:
                continue
            seen.add(lesson_id)
            sources.append({
                "module_id": chunk["module_id"],
                "module_title": chunk["module_title"],
                "lesson_id": lesson_id,
                "lesson_title": chunk["lesson_title"],
            })
        return sources

    def _persist(self, *, conversation, student_id, course_id, question, answer):
        try:
            if conversation is None:
                conversation = AIConversation(student_id=student_id, course_id=course_id)
                db.session.add(conversation)
                db.session.flush()

            db.session.add_all([
                AIMessage(
                    conversation_id=conversation.id,
                    role="USER",
                    content=question,
                ),
                AIMessage(
                    conversation_id=conversation.id,
                    role="ASSISTANT",
                    content=answer,
                ),
            ])
            conversation.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return conversation
        except Exception:
            db.session.rollback()
            raise

    def ask(self, *, student, course, question, conversation_id=None):
        conversation = self._conversation(
            student_id=student.id,
            course_id=course.id,
            conversation_id=conversation_id,
        )

        chunks = CourseRetriever().retrieve(
            course_id=course.id,
            query=question,
            user_id=student.id,
        )

        if not chunks:
            conversation = self._persist(
                conversation=conversation,
                student_id=student.id,
                course_id=course.id,
                question=question,
                answer=INSUFFICIENT_CONTEXT_MESSAGE,
            )
            return {
                "conversation_id": conversation.id,
                "answer": INSUFFICIENT_CONTEXT_MESSAGE,
                "sources": [],
                "insufficient_context": True,
            }

        prompt = build_tutor_prompt(
            retrieved_chunks=chunks,
            question=question,
            conversation_history=self._history_text(conversation),
        )

        answer = LLMService().generate_text(
            system_prompt=TUTOR_SYSTEM_PROMPT,
            user_prompt=prompt,
            feature="rag_tutor",
            user_id=student.id,
            course_id=course.id,
        )

        conversation = self._persist(
            conversation=conversation,
            student_id=student.id,
            course_id=course.id,
            question=question,
            answer=answer,
        )

        return {
            "conversation_id": conversation.id,
            "answer": answer,
            "sources": self._sources(chunks),
            "insufficient_context": False,
        }
