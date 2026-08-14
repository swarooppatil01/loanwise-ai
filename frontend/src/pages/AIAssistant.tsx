import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { chatWithAI } from "../api/ai";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const suggestions = [
  "What can you tell me about my financial profile?",
  "Explain my loan recommendations.",
  "Why was my top recommendation ranked first?",
  "What loan products are available to me?",
];

export default function AIAssistant() {
  const [searchParams] = useSearchParams();

  const applicationIdParam = searchParams.get("application_id");
  const applicationId = applicationIdParam
    ? Number(applicationIdParam)
    : null;

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm LoanWise AI. I can explain your profile, loan applications, and recommendations using your actual LoanWise data.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(
    event?: FormEvent,
    presetMessage?: string,
  ) {
    event?.preventDefault();

    const message = (presetMessage ?? input).trim();

    if (!message || loading) {
      return;
    }

    setError("");
    setInput("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: message,
      },
    ]);

    setLoading(true);

    try {
      const response = await chatWithAI({
        message,
        application_id:
          applicationId && !Number.isNaN(applicationId)
            ? applicationId
            : null,
      });

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.answer,
        },
      ]);
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        "Unable to reach LoanWise AI right now.";

      setError(detail);
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

      <main className="form-page">
        <div className="page-heading">
          <p className="eyebrow">AI assistant</p>

          <h1>Ask LoanWise AI</h1>

          <p>
            Get explanations based on your actual profile,
            applications and LoanWise recommendations.
          </p>
        </div>

        <section className="form-card">
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "16px",
              maxHeight: "520px",
              overflowY: "auto",
              marginBottom: "20px",
            }}
          >
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                style={{
                  alignSelf:
                    message.role === "user"
                      ? "flex-end"
                      : "flex-start",
                  maxWidth: "85%",
                  padding: "14px 16px",
                  borderRadius: "14px",
                  background:
                    message.role === "user"
                      ? "#111827"
                      : "#f3f4f6",
                  color:
                    message.role === "user"
                      ? "white"
                      : "#111827",
                  whiteSpace: "pre-wrap",
                  lineHeight: 1.6,
                }}
              >
                {message.content}
              </div>
            ))}

            {loading && (
              <div
                style={{
                  alignSelf: "flex-start",
                  padding: "14px 16px",
                  borderRadius: "14px",
                  background: "#f3f4f6",
                }}
              >
                LoanWise AI is thinking...
              </div>
            )}
          </div>

          {messages.length === 1 && (
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "8px",
                marginBottom: "16px",
              }}
            >
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="secondary-button"
                  onClick={() => sendMessage(undefined, suggestion)}
                  disabled={loading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}

          {error && <div className="error-box">{error}</div>}

          <form onSubmit={sendMessage}>
            <label>
              Ask a question

              <textarea
                value={input}
                onChange={(event) =>
                  setInput(event.target.value)
                }
                placeholder="For example: Why was my top loan recommendation ranked first?"
                rows={4}
                maxLength={4000}
                disabled={loading}
              />
            </label>

            <button
              type="submit"
              disabled={loading || !input.trim()}
            >
              {loading ? "Analyzing..." : "Ask LoanWise AI →"}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
