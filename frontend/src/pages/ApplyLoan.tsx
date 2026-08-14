import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createApplication } from "../api/applications";

export default function ApplyLoan() {
  const navigate = useNavigate();

  const [loanType, setLoanType] = useState("personal");
  const [amount, setAmount] = useState("");
  const [tenure, setTenure] = useState("36");
  const [purpose, setPurpose] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const application = await createApplication({
        loan_type: loanType,
        loan_amount: Number(amount),
        preferred_tenure_months: Number(tenure),
        purpose,
      });

      navigate(`/recommendations/${application.id}`);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to process your application.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to="/dashboard" className="logo">
          LoanWise AI
        </Link>
        <Link to="/dashboard" className="secondary-link">
          Dashboard
        </Link>
      </header>

      <main className="form-page narrow">
        <div className="page-heading">
          <p className="eyebrow">Loan application</p>
          <h1>What are you looking for?</h1>
          <p>
            We'll compare your request against available LoanWise
            products.
          </p>
        </div>

        <form className="form-card" onSubmit={handleSubmit}>
          <label>
            Loan type
            <select
              value={loanType}
              onChange={(e) => setLoanType(e.target.value)}
            >
              <option value="personal">Personal</option>
              <option value="home">Home</option>
              <option value="education">Education</option>
              <option value="vehicle">Vehicle</option>
            </select>
          </label>

          <label>
            Loan amount
            <input
              type="number"
              min="1"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="500000"
              required
            />
          </label>

          <label>
            Preferred tenure (months)
            <input
              type="number"
              min="1"
              value={tenure}
              onChange={(e) => setTenure(e.target.value)}
              placeholder="36"
              required
            />
          </label>

          <label>
            Purpose
            <textarea
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              placeholder="Home renovation"
              rows={4}
              minLength={3}
              maxLength={500}
              required
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button disabled={loading}>
            {loading
              ? "Analyzing your options..."
              : "Get recommendations →"}
          </button>
        </form>
      </main>
    </div>
  );
}
