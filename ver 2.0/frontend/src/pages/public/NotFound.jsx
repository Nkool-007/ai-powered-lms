import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="container py-5 text-center">
      <div className="display-1 fw-bold">
        404
      </div>

      <h1>Page Not Found</h1>

      <p className="text-secondary">
        The requested page does not exist.
      </p>

      <Link
        to="/"
        className="btn btn-primary"
      >
        Go Home
      </Link>
    </div>
  );
}
