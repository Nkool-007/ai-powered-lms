import {
  useEffect,
  useState,
} from "react";

import {
  Link,
  useParams,
} from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import courseService from "../../services/courseService";
import enrollmentService from "../../services/enrollmentService";
import quizService from "../../services/quizService";

import LoadingSpinner from "../../components/common/LoadingSpinner";
import ErrorState from "../../components/common/ErrorState";
import Button from "../../components/common/Button";

import { getErrorMessage } from "../../utils/errors";

export default function CoursePage() {
  const { courseId } = useParams();

  const {
    user,
    isAuthenticated,
  } = useAuth();

  const [course, setCourse] =
    useState(null);
  const [modules, setModules] =
    useState([]);
  const [quizzes, setQuizzes] =
    useState([]);
  const [enrolled, setEnrolled] =
    useState(false);
  const [loading, setLoading] =
    useState(true);
  const [enrolling, setEnrolling] =
    useState(false);
  const [error, setError] =
    useState("");

  async function loadProtectedStudentData() {
    if (user?.role !== "STUDENT") {
      return;
    }

    const myCourses =
      await enrollmentService.getMyCourses();

    const currentEnrollment =
      myCourses.find(
        (item) =>
          Number(item.course_id) ===
          Number(courseId)
      );

    const isEnrolled =
      Boolean(currentEnrollment);

    setEnrolled(isEnrolled);

    if (isEnrolled) {
      const courseQuizzes =
        await quizService.getCourseQuizzes(
          courseId
        );

      setQuizzes(courseQuizzes);
    } else {
      setQuizzes([]);
    }
  }

  async function load() {
    try {
      setLoading(true);
      setError("");

      const [
        courseData,
        outline,
      ] = await Promise.all([
        courseService.getCourse(courseId),
        courseService.getCourseOutline(
          courseId
        ),
      ]);

      setCourse(courseData);
      setModules(outline);

      try {
        await loadProtectedStudentData();
      } catch (studentError) {
        if (
          studentError?.response?.status !==
          401
        ) {
          setError(
            getErrorMessage(
              studentError,
              "Unable to load enrollment information."
            )
          );
        }
      }
    } catch (requestError) {
      setError(
        getErrorMessage(
          requestError,
          "Unable to load course."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [courseId, user?.id]);

  async function handleEnroll() {
    try {
      setEnrolling(true);
      setError("");

      await enrollmentService.enroll(
        courseId
      );

      setEnrolled(true);

      const courseQuizzes =
        await quizService.getCourseQuizzes(
          courseId
        );

      setQuizzes(courseQuizzes);
    } catch (requestError) {
      if (
        requestError?.response?.data?.error ===
        "ALREADY_ENROLLED"
      ) {
        setEnrolled(true);

        try {
          const courseQuizzes =
            await quizService.getCourseQuizzes(
              courseId
            );
          setQuizzes(courseQuizzes);
        } catch {
          // Enrollment status is still known.
        }

        return;
      }

      setError(
        getErrorMessage(
          requestError,
          "Enrollment failed."
        )
      );
    } finally {
      setEnrolling(false);
    }
  }

  if (loading) {
    return (
      <LoadingSpinner text="Loading course..." />
    );
  }

  if (!course) {
    return (
      <div className="container py-5">
        <ErrorState
          message={
            error ||
            "Course could not be loaded."
          }
          onRetry={load}
        />
      </div>
    );
  }

  const allLessons =
    modules.flatMap(
      (module) =>
        module.lessons || []
    );

  const firstLesson =
    allLessons[0];

  return (
    <div className="container py-5">
      {error && (
        <ErrorState message={error} />
      )}

      <div className="row g-5">
        <div className="col-lg-8">
          <h1>{course.title}</h1>

          <p className="lead">
            {course.description}
          </p>

          {course.instructor && (
            <p className="text-secondary">
              Instructor:{" "}
              {course.instructor.name}
            </p>
          )}

          <h2 className="h4 mt-5">
            Course Content
          </h2>

          {modules.length === 0 && (
            <p className="text-secondary">
              No modules are currently available.
            </p>
          )}

          {modules.map((module) => (
            <div
              key={module.id}
              className="card mb-3"
            >
              <div className="card-body">
                <h3 className="h5">
                  {module.position}.{" "}
                  {module.title}
                </h3>

                <p className="text-secondary">
                  {module.description}
                </p>

                <div className="list-group">
                  {(module.lessons || []).map(
                    (lesson) => (
                      <div
                        key={lesson.id}
                        className="list-group-item"
                      >
                        {lesson.position}.{" "}
                        {lesson.title}
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          ))}

          {user?.role === "STUDENT" &&
            enrolled && (
              <>
                <h2 className="h4 mt-5">
                  Course Quizzes
                </h2>

                {quizzes.length === 0 ? (
                  <p className="text-secondary">
                    No quizzes are available yet.
                  </p>
                ) : (
                  <div className="list-group">
                    {quizzes.map((quiz) => (
                      <Link
                        key={quiz.id}
                        to={`/quizzes/${quiz.id}`}
                        className={
                          "list-group-item " +
                          "list-group-item-action"
                        }
                      >
                        {quiz.title}
                      </Link>
                    ))}
                  </div>
                )}
              </>
            )}
        </div>

        <aside className="col-lg-4">
          <div className="card shadow-sm sticky-lg-top course-action-card">
            <div className="card-body">
              {!isAuthenticated && (
                <Link
                  to="/login"
                  state={{
                    from:
                      `/courses/${courseId}`,
                  }}
                  className="btn btn-primary w-100"
                >
                  Login to Enroll
                </Link>
              )}

              {user?.role === "STUDENT" &&
                !enrolled && (
                  <Button
                    className="w-100"
                    loading={enrolling}
                    onClick={handleEnroll}
                  >
                    Enroll
                  </Button>
                )}

              {user?.role === "STUDENT" &&
                enrolled &&
                firstLesson && (
                  <Link
                    to={
                      `/courses/${courseId}` +
                      `/lessons/${firstLesson.id}`
                    }
                    className="btn btn-success w-100"
                  >
                    Continue Learning
                  </Link>
                )}

              {user?.role === "STUDENT" &&
                enrolled &&
                !firstLesson && (
                  <div className="alert alert-info mb-0">
                    You are enrolled. Lessons
                    will appear when available.
                  </div>
                )}

              {user?.role === "INSTRUCTOR" &&
                Number(course.instructor_id) ===
                Number(user.id) && (
                  <Link
                    to={
                      `/instructor/courses/` +
                      `${courseId}/edit`
                    }
                    className="btn btn-primary w-100"
                  >
                    Manage Course
                  </Link>
                )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
