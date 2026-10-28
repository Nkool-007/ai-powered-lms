import {
  useEffect,
  useState,
} from "react";

import { Link } from "react-router-dom";

import enrollmentService from "../../services/enrollmentService";
import { getErrorMessage } from "../../utils/errors";

import CourseCard from "../../components/course/CourseCard";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";

export default function MyCourses() {
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
        await enrollmentService.getMyCourses();

      setCourses(data);
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to load your courses."
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
      <LoadingSpinner text="Loading your courses..." />
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
        title="No Enrolled Courses"
        message="Start by exploring the course catalog."
        action={
          <Link
            to="/courses"
            className="btn btn-primary"
          >
            Browse Courses
          </Link>
        }
      />
    );
  }

  return (
    <>
      <h1 className="h2 mb-4">
        My Courses
      </h1>

      <div className="row g-4">
        {courses.map((entry) => (
          <div
            className="col-md-6 col-xl-4"
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
              actionLabel="Continue Learning"
              actionTo={
                `/courses/${entry.course_id}`
              }
            />
          </div>
        ))}
      </div>
    </>
  );
}
