import { useState } from "react";
import Button from "../common/Button";

export default function LessonForm({ moduleId, onSubmit, defaultPosition = 1 }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [position, setPosition] = useState(defaultPosition);
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!title.trim() || !content.trim()) return;
    try {
      setLoading(true);
      await onSubmit(moduleId, { title: title.trim(), content: content.trim(), position: Number(position) });
      setTitle(""); setContent(""); setPosition(Number(position) + 1);
    } finally { setLoading(false); }
  }

  return (
    <form className="border rounded p-3 mt-3" onSubmit={submit}>
      <h5 className="h6">Add Lesson</h5>
      <input className="form-control mb-2" placeholder="Lesson title" value={title} onChange={(event) => setTitle(event.target.value)} required />
      <textarea className="form-control mb-2" rows="5" placeholder="Lesson content" value={content} onChange={(event) => setContent(event.target.value)} required />
      <input type="number" min="1" className="form-control mb-3" value={position} onChange={(event) => setPosition(event.target.value)} />
      <Button type="submit" loading={loading}>Add Lesson</Button>
    </form>
  );
}
