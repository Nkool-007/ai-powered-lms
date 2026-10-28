import {
  useEffect,
  useState,
} from "react";

import Button from "../common/Button";

export default function ModuleForm({
  onSubmit,
  defaultPosition = 1,
}) {
  const [form, setForm] = useState({
    title: "",
    description: "",
    position: defaultPosition,
  });
  const [loading, setLoading] =
    useState(false);
  const [error, setError] =
    useState("");

  useEffect(() => {
    setForm((current) => ({
      ...current,
      position: defaultPosition,
    }));
  }, [defaultPosition]);

  async function submit(event) {
    event.preventDefault();
    setError("");

    if (!form.title.trim()) {
      setError("Module title is required.");
      return;
    }

    const position = Number(form.position);

    if (
      !Number.isInteger(position) ||
      position < 1
    ) {
      setError(
        "Module position must be a positive integer."
      );
      return;
    }

    try {
      setLoading(true);

      await onSubmit({
        title: form.title.trim(),
        description:
          form.description.trim(),
        position,
      });

      setForm({
        title: "",
        description: "",
        position: defaultPosition + 1,
      });
    } catch {
      // Parent handles API error.
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      className="border rounded p-3"
      onSubmit={submit}
    >
      <h4 className="h6">
        Add Module
      </h4>

      {error && (
        <div className="alert alert-danger py-2">
          {error}
        </div>
      )}

      <input
        className="form-control mb-2"
        placeholder="Module title"
        value={form.title}
        onChange={(event) =>
          setForm({
            ...form,
            title: event.target.value,
          })
        }
        required
      />

      <textarea
        className="form-control mb-2"
        placeholder="Description"
        value={form.description}
        onChange={(event) =>
          setForm({
            ...form,
            description:
              event.target.value,
          })
        }
      />

      <input
        type="number"
        min="1"
        className="form-control mb-3"
        value={form.position}
        onChange={(event) =>
          setForm({
            ...form,
            position:
              event.target.value,
          })
        }
      />

      <Button
        type="submit"
        loading={loading}
      >
        Add Module
      </Button>
    </form>
  );
}
