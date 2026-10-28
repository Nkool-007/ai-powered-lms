import {
  Link,
  NavLink,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const {
    user,
    isAuthenticated,
    logout,
  } = useAuth();

  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link
          className="navbar-brand fw-bold"
          to="/"
        >
          SmartLMS
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNavbar"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div
          className="collapse navbar-collapse"
          id="mainNavbar"
        >
          <div className="navbar-nav ms-auto align-items-lg-center">
            <NavLink
              className="nav-link"
              to="/courses"
            >
              Courses
            </NavLink>

            {!isAuthenticated && (
              <>
                <NavLink
                  className="nav-link"
                  to="/login"
                >
                  Login
                </NavLink>

                <NavLink
                  className="nav-link"
                  to="/register"
                >
                  Register
                </NavLink>
              </>
            )}

            {user?.role === "STUDENT" && (
              <>
                <NavLink
                  className="nav-link"
                  to="/student/courses"
                >
                  My Courses
                </NavLink>

                <NavLink
                  className="nav-link"
                  to="/student/dashboard"
                >
                  Dashboard
                </NavLink>
              </>
            )}

            {user?.role === "INSTRUCTOR" && (
              <>
                <NavLink
                  className="nav-link"
                  to="/instructor/dashboard"
                >
                  Dashboard
                </NavLink>

                <NavLink
                  className="nav-link"
                  to="/instructor/courses/new"
                >
                  Create Course
                </NavLink>
              </>
            )}

            {isAuthenticated && (
              <button
                type="button"
                onClick={handleLogout}
                className="btn btn-light btn-sm ms-lg-3"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
