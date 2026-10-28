import {
  useEffect,
  useState,
} from "react";

import { Link } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import enrollmentService from "../../services/enrollmentService";
import quizService from "../../services/quizService";
import { getErrorMessage } from "../../utils/errors";
import { formatDateTime } from "../../utils/date";

import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";

export default function StudentDashboard() {
  const { user } = useAuth();

  const [courses, setCourses] =
    useState([]);
  const [attempts, setAttempts] =
    useState([]);
  const [loading, setLoading] =
    useState(true);
  const [error, setError] =
    useState("");

  async function load() {
    try {
      setLoading(true);
      setError("");

      const [
        myCourses,
        myAttempts,
      ] = await Promise.all([
        enrollmentService.getMyCourses(),
        quizService.getMyAttempts(),
      ]);

      setCourses(myCourses);
      setAttempts(
        myAttempts.slice(0, 5)
      );
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load dashboard."
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
      <LoadingSpinner text="Loading dashboard..." />
    );
  }

  return (
    <div>
      <h1 className="h2">
        Welcome, {user.name}
      </h1>

      <p className="text-secondary">
        Continue your learning.
      </p>

      {error && (
        <ErrorState
          message={error}
          onRetry={load}
        />
      )}

      <hr />

      <h2 className="h4 mb-3">
        My Courses
      </h2>

      {courses.length === 0 ? (
        <EmptyState
          title="No Enrolled Courses"
          message="You are not enrolled in any courses yet."
          action={
            <Link
              to="/courses"
              className="btn btn-primary"
            >
              Browse Courses
            </Link>
          }
        />
      ) : (
        <div className="row g-4">
          {courses.map((entry) => (
            <div
              className="col-md-6"
              key={entry.course_id}
            >
              <CourseCard
                course={
                  entry.course || {
                    id: entry.course_id,
                    title: entry.title,
                    description:
                      entry.description,
                  }
                }
                progress={
                  entry.progress_percentage
                }
                actionLabel="Continue"
                actionTo={
                  `/courses/${entry.course_id}`
                }
              />
            </div>
          ))}
        </div>
      )}

      <h2 className="h4 mt-5 mb-3">
        Recent Quiz Attempts
      </h2>

      {attempts.length === 0 ? (
        <p className="text-secondary">
          No quiz attempts yet.
        </p>
      ) : (
        <div className="table-responsive">
          <table className="table">
            <thead>
              <tr>
                <th>Quiz</th>
                <th>Score</th>
                <th>Submitted</th>
              </tr>
            </thead>

            <tbody>
              {attempts.map((attempt) => (
                <tr
                  key={attempt.attempt_id}
                >
                  <td>
                    {attempt.quiz_title}
                  </td>
                  <td>
                    {attempt.score}%
                  </td>
                  <td>
                    {formatDateTime(
                      attempt.submitted_at
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
