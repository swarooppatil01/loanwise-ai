from app.rag.retriever import search_knowledge_base


def search_loanwise_knowledge(
    query: str,
) -> dict:
    """
    Search the LoanWise documentation knowledge base.

    Use this only for general LoanWise documentation,
    policies, methodology, FAQs, and explanations.

    Do NOT use this tool for current loan products,
    interest rates, fees, eligibility, application status,
    or recommendation scores.
    """

    results = search_knowledge_base(
        query=query,
        limit=3,
    )

    if not results:
        return {
            "found": False,
            "message": (
                "No relevant LoanWise documentation was found."
            ),
        }

    return {
        "found": True,
        "results": [
            {
                "document": result["document"],
                "score": result["score"],
                "content": result["content"],
            }
            for result in results
        ],
    }
