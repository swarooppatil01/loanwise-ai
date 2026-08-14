import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";
import { getProfile, updateProfile, type EmploymentType } from "../api/profile";

const initialState: {
  age: string;
  city: string;
  employment_type: EmploymentType | "";
  monthly_income: string;
  monthly_obligations: string;
  credit_score: string;
  employment_duration_months: string;
} = {
  age: "",
  city: "",
  employment_type: "salaried",
  monthly_income: "",
  monthly_obligations: "",
  credit_score: "",
  employment_duration_months: "",
};

export default function Profile() {
  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const profile = await getProfile();

        if (profile) {
          setForm({
            age: profile.age?.toString() ?? "",
            city: profile.city ?? "",
            employment_type:
              profile.employment_type ?? "salaried",
            monthly_income:
              profile.monthly_income ?? "",
            monthly_obligations:
              profile.monthly_obligations ?? "",
            credit_score:
              profile.credit_score?.toString() ?? "",
            employment_duration_months:
              profile.employment_duration_months?.toString() ?? "",
          });
        }
      } catch {
        setError("Unable to load your profile.");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  function update(key: keyof typeof form, value: string) {
    setForm((current) => ({
      ...current,
      [key]: value,
    }));
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    setSaving(true);
    setMessage("");
    setError("");

    try {
      await updateProfile({
        age: form.age ? Number(form.age) : null,
        city: form.city || null,
        employment_type:
          form.employment_type === ""
            ? null
            : form.employment_type,
        monthly_income: form.monthly_income
          ? Number(form.monthly_income)
          : null,
        monthly_obligations: form.monthly_obligations
          ? Number(form.monthly_obligations)
          : null,
        credit_score: form.credit_score
          ? Number(form.credit_score)
          : null,
        employment_duration_months:
          form.employment_duration_months
            ? Number(form.employment_duration_months)
            : null,
      });

      setMessage("Profile saved successfully.");
    } catch {
      setError("Unable to save your profile.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <div className="loading-page">Loading profile...</div>;
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

      <main className="form-page">
        <div className="page-heading">
          <p className="eyebrow">Your financial profile</p>
          <h1>Complete your profile</h1>
          <p>
            These details are used by the recommendation engine to
            evaluate available products.
          </p>
        </div>

        <form className="form-card" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label>
              Age
              <input
                type="number"
                min="18"
                max="100"
                value={form.age}
                onChange={(e) => update("age", e.target.value)}
                required
              />
            </label>

            <label>
              City
              <input
                value={form.city}
                onChange={(e) => update("city", e.target.value)}
                placeholder="Pune"
                required
              />
            </label>

            <label>
              Employment type
              <select
                value={form.employment_type}
                onChange={(e) =>
                  update("employment_type", e.target.value)
                }
              >
                <option value="salaried">Salaried</option>
                <option value="self_employed">Self employed</option>
                <option value="professional">Professional</option>
                <option value="business_owner">Business owner</option>
                <option value="other">Other</option>
              </select>
            </label>

            <label>
              Monthly income
              <input
                type="number"
                min="0"
                value={form.monthly_income}
                onChange={(e) =>
                  update("monthly_income", e.target.value)
                }
                placeholder="75000"
                required
              />
            </label>

            <label>
              Monthly obligations
              <input
                type="number"
                min="0"
                value={form.monthly_obligations}
                onChange={(e) =>
                  update("monthly_obligations", e.target.value)
                }
                placeholder="10000"
                required
              />
            </label>

            <label>
              Credit score
              <input
                type="number"
                min="300"
                max="900"
                value={form.credit_score}
                onChange={(e) =>
                  update("credit_score", e.target.value)
                }
                placeholder="760"
                required
              />
            </label>

            <label>
              Employment duration (months)
              <input
                type="number"
                min="0"
                max="600"
                value={form.employment_duration_months}
                onChange={(e) =>
                  update(
                    "employment_duration_months",
                    e.target.value,
                  )
                }
                placeholder="24"
                required
              />
            </label>
          </div>

          {message && <div className="success-box">{message}</div>}
          {error && <div className="error-box">{error}</div>}

          <button disabled={saving}>
            {saving ? "Saving..." : "Save profile"}
          </button>
        </form>
      </main>
    </div>
  );
}
