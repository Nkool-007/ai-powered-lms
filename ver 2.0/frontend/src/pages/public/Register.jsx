import { useState } from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import { getErrorMessage } from "../../utils/errors";
import Button from "../../components/common/Button";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] =
    useState({
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      role: "STUDENT",
    });

  const [error, setError] =
    useState("");
  const [loading, setLoading] =
    useState(false);

  function update(event) {
    setForm({
      ...form,
      [event.target.name]:
        event.target.value,
    });
  }

  async function submit(event) {
    event.preventDefault();
    setError("");

    if (
      !form.name.trim() ||
      !form.email.trim() ||
      !form.password
    ) {
      setError(
        "All required fields must be completed."
      );
      return;
    }

    if (form.password.length < 8) {
      setError(
        "Password must contain at least 8 characters."
      );
      return;
    }

    if (
      form.password !==
      form.confirmPassword
    ) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      await register({
        name: form.name.trim(),
        email: form.email.trim(),
        password: form.password,
        role: form.role,
      });

      navigate(
        "/login",
        {
          replace: true,
          state: {
            message:
              "Registration successful. Please login.",
          },
        }
      );
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to register."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container py-5">
      <div className="auth-card mx-auto">
        <h1 className="h3 mb-4">
          Create Account
        </h1>

        {error && (
          <div className="alert alert-danger">
            {error}
          </div>
        )}

        <form onSubmit={submit}>
          <div className="mb-3">
            <label
              className="form-label"
              htmlFor="name"
            >
              Name
            </label>

            <input
              id="name"
              name="name"
              value={form.name}
              onChange={update}
              className="form-control"
              required
            />
          </div>

          <div className="mb-3">
            <label
              className="form-label"
              htmlFor="email"
            >
              Email
            </label>

            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={update}
              className="form-control"
              required
            />
          </div>

          <div className="mb-3">
            <label
              className="form-label"
              htmlFor="password"
            >
              Password
            </label>

            <input
              id="password"
              name="password"
              type="password"
              value={form.password}
              onChange={update}
              className="form-control"
              required
            />
          </div>

          <div className="mb-3">
            <label
              className="form-label"
              htmlFor="confirmPassword"
            >
              Confirm Password
            </label>

            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={form.confirmPassword}
              onChange={update}
              className="form-control"
              required
            />
          </div>

          <div className="mb-3">
            <label
              className="form-label"
              htmlFor="role"
            >
              Account Type
            </label>

            <select
              id="role"
              name="role"
              className="form-select"
              value={form.role}
              onChange={update}
            >
              <option value="STUDENT">
                Student
              </option>
              <option value="INSTRUCTOR">
                Instructor
              </option>
            </select>
          </div>

          <Button
            type="submit"
            loading={loading}
            className="w-100"
          >
            Register
          </Button>
        </form>

        <p className="mt-3 mb-0">
          Already registered?{" "}
          <Link to="/login">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
