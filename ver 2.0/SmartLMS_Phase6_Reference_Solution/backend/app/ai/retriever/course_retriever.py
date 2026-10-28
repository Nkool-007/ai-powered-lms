from flask import current_app

from app.extensions import db
from app.models import CourseChunk
from app.ai.services.llm_service import LLMService


class CourseRetriever:
    def retrieve(self, *, course_id, query, user_id=None):
        query_embedding = LLMService().embed_text(
            query,
            feature="tutor_query_embedding",
            user_id=user_id,
            course_id=course_id,
        )

        top_k = current_app.config["RAG_TOP_K"]
        max_distance = current_app.config["RAG_MAX_COSINE_DISTANCE"]

        distance = CourseChunk.embedding.cosine_distance(query_embedding).label("distance")

        rows = (
            db.session.query(CourseChunk, distance)
            .filter(CourseChunk.course_id == course_id)
            .order_by(distance.asc())
            .limit(top_k)
            .all()
        )

        results = []
        for chunk, score in rows:
            score = float(score)
            if score > max_distance:
                continue

            results.append({
                "chunk_id": chunk.chunk_id,
                "course_id": chunk.course_id,
                "module_id": chunk.module_id,
                "module_title": chunk.module_title,
                "lesson_id": chunk.lesson_id,
                "lesson_title": chunk.lesson_title,
                "content": chunk.content,
                "distance": score,
            })

        return results
