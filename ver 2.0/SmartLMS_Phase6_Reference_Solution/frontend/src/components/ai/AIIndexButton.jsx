import { useState } from "react";

import aiService from "../../services/aiService";


export default function AIIndexButton({ courseId }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function rebuild() {
    try {
      setLoading(true);
      setMessage("");
      const result = await aiService.reindexCourse(courseId);
      setMessage(`${result.chunks_indexed} chunks indexed.`);
    } catch {
      setMessage("Could not rebuild AI index.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        className="btn btn-outline-primary"
        onClick={rebuild}
        disabled={loading}
      >
        {loading ? "Indexing..." : "Rebuild Course AI Index"}
      </button>

      {message && <p className="small mt-2">{message}</p>}
    </div>
  );
}
