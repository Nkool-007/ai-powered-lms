import hashlib
import re

from flask import current_app

from app.extensions import db
from app.models import CourseChunk, Lesson, Module
from app.ai.services.llm_service import LLMService


def clean_text(text):
    if not text:
        return ""

    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def chunk_text(text, *, max_words, overlap_words):
    words = text.split()
    if not words:
        return []

    if max_words <= overlap_words:
        raise ValueError("max_words must be greater than overlap_words.")

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_words, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap_words

    return chunks


def index_course(course):
    if course.status != "PUBLISHED":
        raise ValueError("Only published Courses can be indexed.")

    max_words = current_app.config["RAG_CHUNK_WORDS"]
    overlap_words = current_app.config["RAG_CHUNK_OVERLAP_WORDS"]

    lesson_rows = (
        db.session.query(Lesson, Module)
        .join(Module, Lesson.module_id == Module.id)
        .filter(Module.course_id == course.id)
        .order_by(Module.position.asc(), Lesson.position.asc())
        .all()
    )

    prepared = []

    for lesson, module in lesson_rows:
        cleaned = clean_text(lesson.content)
        chunks = chunk_text(
            cleaned,
            max_words=max_words,
            overlap_words=overlap_words,
        )

        for index, content in enumerate(chunks, start=1):
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            prepared.append({
                "chunk_id": f"{course.id}:{module.id}:{lesson.id}:{index}",
                "course_id": course.id,
                "module_id": module.id,
                "lesson_id": lesson.id,
                "module_title": module.title,
                "lesson_title": lesson.title,
                "content": content,
                "content_hash": content_hash,
            })

    if not prepared:
        return {"course_id": course.id, "chunks_indexed": 0}

    texts = [item["content"] for item in prepared]
    embeddings = LLMService().embed_texts(
        texts,
        feature="course_indexing",
        course_id=course.id,
    )

    if len(embeddings) != len(prepared):
        raise RuntimeError("Embedding count does not match chunk count.")

    # Generate the new embeddings before deleting the previous index.
    # A provider failure therefore does not destroy the last usable index.
    try:
        CourseChunk.query.filter_by(course_id=course.id).delete(synchronize_session=False)
        records = [
            CourseChunk(**item, embedding=embedding)
            for item, embedding in zip(prepared, embeddings)
        ]
        db.session.add_all(records)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {"course_id": course.id, "chunks_indexed": len(records)}
