import {
  useEffect,
  useState,
} from "react";

import Button from "../common/Button";

export default function LessonForm({
  moduleId,
  onSubmit,
  defaultPosition = 1,
}) {
  const [title, setTitle] =
    useState("");
  const [content, setContent] =
    useState("");
  const [position, setPosition] =
    useState(defaultPosition);
  const [loading, setLoading] =
    useState(false);
  const [error, setError] =
    useState("");

  useEffect(() => {
    setPosition(defaultPosition);
  }, [defaultPosition]);

  async function submit(event) {
    event.preventDefault();
    setError("");

    if (!title.trim() || !content.trim()) {
      setError(
        "Lesson title and content are required."
      );
      return;
    }

    const numericPosition =
      Number(position);

    if (
      !Number.isInteger(numericPosition) ||
      numericPosition < 1
    ) {
      setError(
        "Lesson position must be a positive integer."
      );
      return;
    }

    try {
      setLoading(true);

      await onSubmit(
        moduleId,
        {
          title: title.trim(),
          content: content.trim(),
          position: numericPosition,
        }
      );

      setTitle("");
      setContent("");
      setPosition(numericPosition + 1);
    } catch {
      // Parent handles API error.
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      className="border rounded p-3 mt-3"
      onSubmit={submit}
    >
      <h5 className="h6">
        Add Lesson
      </h5>

      {error && (
        <div className="alert alert-danger py-2">
          {error}
        </div>
      )}

      <input
        className="form-control mb-2"
        placeholder="Lesson title"
        value={title}
        onChange={(event) =>
          setTitle(event.target.value)
        }
        required
      />

      <textarea
        className="form-control mb-2"
        rows="5"
        placeholder="Lesson content"
        value={content}
        onChange={(event) =>
          setContent(event.target.value)
        }
        required
      />

      <input
        type="number"
        min="1"
        className="form-control mb-3"
        value={position}
        onChange={(event) =>
          setPosition(event.target.value)
        }
      />

      <Button
        type="submit"
        loading={loading}
      >
        Add Lesson
      </Button>
    </form>
  );
}
