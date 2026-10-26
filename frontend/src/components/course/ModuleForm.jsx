import { useState } from "react";
import Button from "../common/Button";

export default function ModuleForm({ onSubmit, defaultPosition = 1 }) {
  const [form, setForm] = useState({ title: "", description: "", position: defaultPosition });
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!form.title.trim()) return;
    try {
      setLoading(true);
      await onSubmit({ title: form.title.trim(), description: form.description.trim(), position: Number(form.position) });
      setForm({ title: "", description: "", position: defaultPosition + 1 });
    } finally { setLoading(false); }
  }

  return (
    <form className="border rounded p-3" onSubmit={submit}>
      <h4 className="h6">Add Module</h4>
      <input className="form-control mb-2" placeholder="Module title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required />
      <textarea className="form-control mb-2" placeholder="Description" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
      <input type="number" min="1" className="form-control mb-3" value={form.position} onChange={(event) => setForm({ ...form, position: event.target.value })} />
      <Button type="submit" loading={loading}>Add Module</Button>
    </form>
  );
}
