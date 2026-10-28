import { Link } from "react-router-dom";

export default function Home() {
  return (
    <>
      <section className="hero-section">
        <div className="container py-5">
          <div className="row align-items-center min-vh-50">
            <div className="col-lg-7">
              <span className="badge text-bg-light text-primary mb-3">
                EDUZZA SmartLMS
              </span>

              <h1 className="display-4 fw-bold">
                Learn with structure. Understand with intelligence.
              </h1>

              <p className="lead mt-3">
                Study structured courses, track your progress,
                test your understanding, and prepare for the
                later AI-assisted learning layer.
              </p>

              <div className="d-flex gap-2 flex-wrap mt-4">
                <Link
                  to="/courses"
                  className="btn btn-light btn-lg"
                >
                  Explore Courses
                </Link>

                <Link
                  to="/register"
                  className="btn btn-outline-light btn-lg"
                >
                  Create Account
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="container py-5">
        <div className="row g-4">
          <div className="col-md-6">
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h2 className="h4">
                  For Students
                </h2>
                <p>
                  Discover courses, complete lessons,
                  attempt quizzes, and understand your
                  learning progress.
                </p>
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h2 className="h4">
                  For Instructors
                </h2>
                <p>
                  Create structured courses, organize
                  lessons, build quizzes, publish content,
                  and monitor learners.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
