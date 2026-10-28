import { useEffect, useState } from "react";

import aiService from "../../services/aiService";
import enrollmentService from "../../services/enrollmentService";
import { getErrorMessage } from "../../utils/errors";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";
import EmptyState from "../../components/common/EmptyState";


export default function AITutor() {
  const [courses, setCourses] = useState([]);
  const [courseId, setCourseId] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    enrollmentService
      .getMyCourses()
      .then((result) => {
        setCourses(result);
        if (result.length > 0) {
          setCourseId(String(result[0].course_id));
        }
      })
      .catch((err) => {
        setError(getErrorMessage(err, "Could not load Courses."));
      })
      .finally(() => setLoadingCourses(false));
  }, []);

  function changeCourse(event) {
    setCourseId(event.target.value);
    setConversationId(null);
    setMessages([]);
    setError("");
  }

  async function send(event) {
    event.preventDefault();
    const message = input.trim();
    if (!message || !courseId) return;

    setMessages((current) => [...current, { role: "USER", content: message }]);
    setInput("");

    try {
      setSending(true);
      setError("");

      const result = await aiService.chat({
        courseId: Number(courseId),
        message,
        conversationId,
      });

      setConversationId(result.conversation_id);
      setMessages((current) => [
        ...current,
        {
          role: "ASSISTANT",
          content: result.answer,
          sources: result.sources,
          insufficientContext: result.insufficient_context,
        },
      ]);
    } catch (err) {
      setError(getErrorMessage(err, "The AI Tutor could not answer."));
    } finally {
      setSending(false);
    }
  }

  if (loadingCourses) {
    return <LoadingSpinner text="Loading your Courses..." />;
  }

  if (courses.length === 0) {
    return (
      <EmptyState
        title="No Enrolled Courses"
        message="Enroll in a Course before using the Course-Aware AI Tutor."
      />
    );
  }

  return (
    <div className="container py-4">
      <h1 className="h2">Course-Aware AI Tutor</h1>
      <p className="text-secondary">
        Ask questions about a Course in which you are enrolled.
      </p>

      <label className="form-label">Current Course</label>
      <select
        className="form-select mb-4"
        value={courseId}
        onChange={changeCourse}
      >
        {courses.map((course) => (
          <option key={course.course_id} value={course.course_id}>
            {course.title}
          </option>
        ))}
      </select>

      {error && <ErrorState message={error} />}

      <div className="card mb-3">
        <div className="card-body" style={{ minHeight: "360px" }}>
          {messages.length === 0 && (
            <p className="text-secondary">Ask your first Course question.</p>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={message.role === "USER" ? "mb-4 text-end" : "mb-4"}
            >
              <strong>{message.role === "USER" ? "You" : "AI Tutor"}</strong>
              <p className="mb-2">{message.content}</p>

              {message.sources?.length > 0 && (
                <div className="small text-secondary">
                  <strong>Sources</strong>
                  <ul>
                    {message.sources.map((source) => (
                      <li key={source.lesson_id}>
                        {source.module_title} {" → "} {source.lesson_title}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}

          {sending && <p className="text-secondary">Tutor is thinking...</p>}
        </div>
      </div>

      <form onSubmit={send}>
        <div className="input-group">
          <textarea
            className="form-control"
            rows="2"
            value={input}
            placeholder="Ask a question about this Course..."
            onChange={(event) => setInput(event.target.value)}
          />
          <button className="btn btn-primary" disabled={sending}>
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
