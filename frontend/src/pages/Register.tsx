import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../api/auth";

export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      await register({
        full_name: name,
        email,
        password,
      });

      navigate("/login");
    } catch {
      setError("Unable to create account. Please check your details.");
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
            <p>Build your personalized loan profile</p>
          </div>
        </div>

        <h2>Create account</h2>
        <p className="muted">
          Start by creating your LoanWise account.
        </p>

        <form onSubmit={handleSubmit}>
          <label>
            Full name
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Your name"
              required
            />
          </label>

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
              minLength={8}
              required
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button disabled={loading}>
            {loading ? "Creating..." : "Create account"}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </section>
    </main>
  );
}
