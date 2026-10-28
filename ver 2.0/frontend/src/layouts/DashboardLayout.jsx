import {
  NavLink,
  Outlet,
} from "react-router-dom";

export default function DashboardLayout({
  role,
}) {
  const studentLinks = [
    ["/student/dashboard", "Dashboard"],
    ["/student/courses", "My Courses"],
    ["/student/progress", "Progress"],
    ["/student/ai", "AI Tutor"],
  ];

  const instructorLinks = [
    ["/instructor/dashboard", "Dashboard"],
    ["/instructor/courses/new", "Create Course"],
    ["/instructor/ai-quiz", "AI Quiz Generator"],
  ];

  const links =
    role === "STUDENT"
      ? studentLinks
      : instructorLinks;

  return (
    <div className="container-fluid">
      <div className="row">
        <aside className="col-lg-2 dashboard-sidebar p-3">
          <div className="nav flex-column nav-pills">
            {links.map(([path, label]) => (
              <NavLink
                key={path}
                to={path}
                className="nav-link"
              >
                {label}
              </NavLink>
            ))}
          </div>
        </aside>

        <section className="col-lg-10 p-4">
          <Outlet />
        </section>
      </div>
    </div>
  );
}
