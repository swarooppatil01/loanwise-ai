import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  getApplication,
  type LoanApplication,
  type Recommendation,
} from "../api/applications";

function money(value: string) {
  return Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  });
}

export default function Recommendations() {
  const { applicationId } = useParams();

  const [application, setApplication] =
    useState<LoanApplication | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!applicationId) return;

    getApplication(Number(applicationId))
      .then(setApplication)
      .catch(() => setError("Unable to load recommendations."));
  }, [applicationId]);

  if (error) {
    return <div className="loading-page">{error}</div>;
  }

  if (!application) {
    return (
      <div className="loading-page">
        Loading recommendations...
      </div>
    );
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

      <main className="recommendations-page">
        <div className="ai-recommendation-action">
          <Link
            to={`/ai?application_id=${application.id}`}
            className="secondary-link"
          >
            Explain this recommendation with AI →
          </Link>
        </div>
        <section className="page-heading">
          <p className="eyebrow">Application #{application.id}</p>

          <h1>Your recommended loans</h1>

          <p>
            We compared your application against the available loan
            products using your financial profile.
          </p>
        </section>

        <section className="application-summary">
          <div>
            <span>Requested amount</span>
            <strong>
              ₹{money(application.loan_amount)}
            </strong>
          </div>

          <div>
            <span>Tenure</span>
            <strong>
              {application.preferred_tenure_months} months
            </strong>
          </div>

          <div>           <span>Status</span>
            <strong>{application.status}</strong>
          </div>
        </section>

        <div className="recommendation-list">
          {application.recommendations.map(
            (recommendation: Recommendation) => (
              <article
                className={`recommendation-card ${
                  recommendation.eligible
                    ? "eligible"
                    : "ineligible"
                }`}
                key={recommendation.id}
              >
                <div className="recommendation-top">
                  <div>
                    <span className="rank">
                      #{recommendation.rank}
                    </span>

                    <h2>
                      {recommendation.loan_product.name}
                    </h2>

                    <p>
                      {recommendation.loan_product.lender}
                    </p>
                  </div>

                  <div className="score">
                    <span>Score</span>
                    <strong>
                      {recommendation.score}
                    </strong>
                  </div>
                </div>

                <div className="eligibility">
                  {recommendation.eligible
                    ? "✓ Eligible"
                    : "Not currently eligible"}
                </div>

                <div className="loan-meta">
                  <div>
                    <span>Interest</span>
                    <strong>
                      {recommendation.loan_product.min_interest_rate}%
                      {" – "}
                      {recommendation.loan_product.max_interest_rate}%
                    </strong>
                  </div>

                  <div>
                    <span>Amount</span>
                    <strong>
                      ₹{money(
                        recommendation.loan_product.min_amount,
                      )}
                      {" – ₹"}
                      {money(
              recommendation.loan_product.max_amount,
                      )}
                    </strong>
                  </div>

                  <div>
                    <span>Tenure</span>
                    <strong>
                      {
                        recommendation.loan_product
                          .min_tenure_months
                      }
                      {" – "}
                      {
                        recommendation.loan_product
                          .max_tenure_months
                      }{" "}
                      months
                    </strong>
                  </div>
                </div>

                {recommendation.explanation && (
                  <div className="explanation">
                    <h3>Why?</h3>

                    <p>
                      {recommendation.explanation}
                    </p>
                  </div>
                )}

                <details className="factors">
                  <summary>
                  View scoring factors
                  </summary>

                  {recommendation.factors.map(
                    (factor) => (
                      <div
                        className="factor"
                        key={factor.id}
                      >
                        <div>
                          <strong>
                            {factor.factor}
                          </strong>

                          <span>
                            {factor.reason}
                          </span>
                        </div>

                        <strong>
                          {factor.contribution}
                        </strong>
                      </div>
                    ),
                  )}
                </details>

                {recommendation.eligible && (
                  <button
                    type="button"
                    className="ai-button"
                    onClick={() =>
                      window.location.assign(
                        `/ai?application_id=${application.id}`,
                      )
                    }
                  >
                    Ask LoanWise AI →
                  </button>
                )}
              </article>
            ),
          )}
        </div>
      </main>
    </div>
  );
}
