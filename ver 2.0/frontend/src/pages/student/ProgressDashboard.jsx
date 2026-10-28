import {
  useEffect,
  useState,
} from "react";

import enrollmentService from "../../services/enrollmentService";
import { getErrorMessage } from "../../utils/errors";

import ProgressBar from "../../components/progress/ProgressBar";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";

export default function ProgressDashboard() {
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

      const enrolled =
        await enrollmentService.getMyCourses();

      const detailed =
        await Promise.all(
          enrolled.map(
            async (course) => {
              try {
                const progress =
                  await enrollmentService
                    .getCourseProgress(
                      course.course_id
                    );

                return {
                  ...course,
                  ...progress,
                };
              } catch {
                return course;
              }
            }
          )
        );

      setCourses(detailed);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load progress."
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
      <LoadingSpinner text="Loading progress..." />
    );
  }

  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={load}
      />
    );
  }

  if (courses.length === 0) {
    return (
      <EmptyState
        title="No Progress Yet"
        message="Enroll in a course to begin tracking progress."
      />
    );
  }

  return (
    <>
      <h1 className="h2 mb-4">
        Learning Progress
      </h1>

      <div className="row g-4">
        {courses.map((course) => (
          <div
            className="col-lg-6"
            key={course.course_id}
          >
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h2 className="h5">
                  {course.title}
                </h2>

                <ProgressBar
                  percentage={
                    course.progress_percentage
                  }
                />

                {course.total_lessons !==
                  undefined && (
                  <p className="small text-secondary mt-3 mb-0">
                    {course.completed_lessons}{" "}
                    of{" "}
                    {course.total_lessons}{" "}
                    lessons completed
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
