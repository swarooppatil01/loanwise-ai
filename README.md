# LoanWise AI

LoanWise AI is an AI-powered loan decision-support application that helps users understand their financial profile, submit loan applications, receive deterministic loan recommendations, and ask an AI assistant for explanations based on their actual LoanWise data.

The project combines a deterministic recommendation engine, PostgreSQL-backed application data, Gemini-powered AI assistance, and a Markdown-based RAG knowledge base.

> **Important:** LoanWise AI is a technical/demo decision-support system. Recommendations are not loan approval decisions and do not guarantee approval by a lender.

---

## What is LoanWise AI?

LoanWise AI allows a user to:

- Create and authenticate an account
- Maintain a financial profile
- View their financial information
- Apply for loans
- Compare their application against available loan products
- Receive ranked loan recommendations
- See eligibility and recommendation scores
- Inspect the individual scoring factors behind a recommendation
- Ask LoanWise AI questions about their profile
- Ask why a recommendation was ranked first
- Ask about their previous/current loan applications
- Ask about currently available loan products
- Ask general questions about LoanWise policies and recommendation methodology

The AI assistant does not independently invent loan eligibility decisions.

For authoritative current financial and recommendation information, the AI uses authenticated tools backed by the LoanWise database.

---

# Core Architecture

```text
                         ┌──────────────────────┐
                         │      Frontend        │
                         │ React + TypeScript   │
                         │ Vite + CSS           │
                         └──────────┬───────────┘
                                    │
                              REST API / JWT
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐     ┌────────────────┐    ┌───────────────┐
       │ PostgreSQL   │     │ Recommendation │    │ Gemini AI     │
       │              │     │ Engine         │    │ Agent         │
       │ Users        │     │                │    │               │
       │ Profiles     │     │ Eligibility    │    │ Tool calling  │
       │ Applications │     │ Score          │    │ Explanations  │
       │ Products     │     │ Ranking        │    │               │
       │ Factors      │     └────────────────┘    └───────┬───────┘
       └──────────────┘                                    │
                                                           │
                                            ┌──────────────┴─────────────┐
                                            │                            │
                                            ▼                            ▼
                                   Database Tools                 RAG Knowledge
                                   ──────────────                 ─────────────
                                   Profile                       ai_policy.md
                                   Applications                  loan_products.md
                                   Recommendations               recommendations.md
                                   Loan Products