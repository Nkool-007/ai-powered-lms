import {
  useEffect,
  useState,
} from "react";

import Button from "../common/Button";

export default function CourseForm({
  initialValue,
  onSubmit,
  submitLabel = "Save Course",
}) {
  const [form, setForm] = useState({
    title: "",
    description: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialValue) {
      setForm({
        title: initialValue.title || "",
        description:
          initialValue.description || "",
      });
    }
  }, [initialValue]);

  function update(event) {
    setForm({
      ...form,
      [event.target.name]:
        event.target.value,
    });
  }

  async function submit(event) {
    event.preventDefault();
    setError("");

    if (!form.title.trim()) {
      setError("Course title is required.");
      return;
    }

    if (!form.description.trim()) {
      setError(
        "Course description is required."
      );
      return;
    }

    try {
      setLoading(true);

      await onSubmit({
        title: form.title.trim(),
        description:
          form.description.trim(),
      });
    } catch {
      // Parent displays API errors.
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit}>
      {error && (
        <div className="alert alert-danger">
          {error}
        </div>
      )}

      <div className="mb-3">
        <label
          htmlFor="title"
          className="form-label"
        >
          Course Title
        </label>

        <input
          id="title"
          name="title"
          value={form.title}
          onChange={update}
          className="form-control"
          required
        />
      </div>

      <div className="mb-3">
        <label
          htmlFor="description"
          className="form-label"
        >
          Description
        </label>

        <textarea
          id="description"
          name="description"
          rows="6"
          value={form.description}
          onChange={update}
          className="form-control"
          required
        />
      </div>

      <Button
        type="submit"
        loading={loading}
      >
        {submitLabel}
      </Button>
    </form>
  );
}
