import {
  useEffect,
  useState,
} from "react";

import { Link } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import courseService from "../../services/courseService";
import { getErrorMessage } from "../../utils/errors";

import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";

export default function InstructorDashboard() {
  const { user } = useAuth();

  const [courses, setCourses] =
    useState([]);
  const [loading, setLoading] =
    useState(true);
  const [error, setError] =
    useState("");

  async function load() {
    try {
      setLoading(true);
      setError("");

      const data =
        await courseService
          .getInstructorCourses();

      setCourses(data);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load instructor dashboard."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) {
    return (
      <LoadingSpinner text="Loading instructor dashboard..." />
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-4">
        <div>
          <h1 className="h2">
            Welcome, {user.name}
          </h1>

          <p className="text-secondary mb-0">
            Manage your Courses.
          </p>
        </div>

        <Link
          to="/instructor/courses/new"
          className="btn btn-primary"
        >
          Create New Course
        </Link>
      </div>

      {error && (
        <ErrorState
          message={error}
          onRetry={load}
        />
      )}

      {!error &&
        courses.length === 0 ? (
        <EmptyState
          title="No Courses Yet"
          message="Create your first course to begin."
          action={
            <Link
              to="/instructor/courses/new"
              className="btn btn-primary"
            >
              Create Course
            </Link>
          }
        />
      ) : (
        <div className="row g-4">
          {courses.map((course) => (
            <div
              className="col-md-6"
              key={course.id}
            >
              <CourseCard
                course={course}
                actionLabel="Manage"
                actionTo={
                  `/instructor/courses/` +
                  `${course.id}/edit`
                }
              />
            </div>
          ))}
        </div>
      )}
    </>
  );
}
