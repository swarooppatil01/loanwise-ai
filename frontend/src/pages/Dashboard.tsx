import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to="/dashboard" className="logo">
          LoanWise AI
        </Link>

        <div className="topbar-actions">
          <span>{user?.full_name}</span>
          <button className="secondary-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div>
            <p className="eyebrow">Personalized lending</p>
            <h1>Find the loan that fits you.</h1>
            <p>
              LoanWise analyzes your financial profile and compares
              available loan products using transparent eligibility
              and scoring rules.
            </p>
          </div>

          <Link to="/apply" className="primary-link">
            Apply for a loan →
          </Link>
        </section>

        <section className="dashboard-grid">
          <Link to="/profile" className="dashboard-card">
            <span className="card-icon">01</span>
            <h2>Complete your profile</h2>
            <p>
              Add income, obligations, employment and credit information.
            </p>
          </Link>

          <Link to="/apply" className="dashboard-card">
            <span className="card-icon">02</span>
            <h2>Apply for a loan</h2>
            <p>
              Tell us what you need and let LoanWise compare products.
            </p>
          </Link>

          <div className="dashboard-card">
            <span className="card-icon">03</span>
            <h2>AI assistance</h2>
            <p>
              Ask LoanWise AI why a recommention fits your profile.
            </p>
            <span className="coming-soon">Coming next</span>
          </div>
        </section>
      </main>
    </div>
  );
}
