import { useState } from "react";
import { useNavigate } from "react-router-dom";

import courseService from "../../services/courseService";
import { getErrorMessage } from "../../utils/errors";

import CourseForm from "../../components/course/CourseForm";
import ErrorState from "../../components/common/ErrorState";

export default function CreateCourse() {
  const navigate = useNavigate();
  const [error, setError] =
    useState("");

  async function create(payload) {
    try {
      setError("");

      const course =
        await courseService.createCourse(
          payload
        );

      navigate(
        `/instructor/courses/${course.id}/edit`
      );
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to create course."
        )
      );

      throw err;
    }
  }

  return (
    <div className="editor-width">
      <h1 className="h2 mb-4">
        Create Course
      </h1>

      {error && (
        <ErrorState message={error} />
      )}

      <div className="card">
        <div className="card-body">
          <CourseForm
            onSubmit={create}
            submitLabel="Create Course"
          />
        </div>
      </div>
    </div>
  );
}
