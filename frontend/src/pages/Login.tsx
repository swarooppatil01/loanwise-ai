import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getMe, login } from "../api/auth";
import { useAuthStore } from "../stores/authStore";

export default function Login() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const tokenResponse = await login(email, password);

      localStorage.setItem(
        "loanwise_access_token",
        tokenResponse.access_token,
      );

      const user = await getMe();

      setAuth(tokenResponse.access_token, user);

      navigate("/dashboard");
    } catch {
      localStorage.removeItem("loanwise_access_token");
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="brand">
          <span className="brand-mark">L</span>
          <div>
            <h1>LoanWise AI</h1>
            <p>Intelligent loan recommendations</p>
          </div>
        </div>

        <h2>Welcome back</h2>
        <p className="muted">
          Sign in to view your personalized loan options.
        </p>

        <form onSubmit={handleSubmit}>
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
              required
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="auth-footer">
          Don't have an account? <Link to="/register">Create one</Link>
        </p>
      </section>
    </main>
  );
}
