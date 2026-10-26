import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { getErrorMessage } from "../../utils/errors";
import Button from "../../components/common/Button";

export default function Login() {
  const { login, user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated && user) return <Navigate to={user.role === "STUDENT" ? "/student/dashboard" : "/instructor/dashboard"} replace />;

  async function submit(event) {
    event.preventDefault(); setError("");
    if (!email.trim() || !password) return setError("Email and password are required.");
    try {
      setLoading(true);
      const loggedInUser = await login({ email: email.trim(), password });
      const requestedRoute = location.state?.from;
      if (requestedRoute) return navigate(requestedRoute, { replace: true });
      navigate(loggedInUser.role === "STUDENT" ? "/student/dashboard" : "/instructor/dashboard", { replace: true });
    } catch (err) { setError(getErrorMessage(err, "Unable to login.")); }
    finally { setLoading(false); }
  }

  return <div className="container py-5"><div className="auth-card mx-auto"><h1 className="h3 mb-4">Login</h1>{error && <div className="alert alert-danger" role="alert">{error}</div>}<form onSubmit={submit}><div className="mb-3"><label className="form-label" htmlFor="email">Email</label><input id="email" type="email" className="form-control" value={email} onChange={(e)=>setEmail(e.target.value)} required /></div><div className="mb-3"><label className="form-label" htmlFor="password">Password</label><input id="password" type="password" className="form-control" value={password} onChange={(e)=>setPassword(e.target.value)} required /></div><Button type="submit" loading={loading} className="w-100">Login</Button></form><p className="mt-3 mb-0">New user? <Link to="/register">Create an account</Link></p></div></div>;
}
