from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "loanwise"


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if len(token) > 2
    }


def search_knowledge_base(
    query: str,
    limit: int = 3,
) -> list[dict]:
    query_tokens = _tokens(query)

    if not query_tokens:
        return []

    results = []

    for path in KNOWLEDGE_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        tokens = _tokens(text)

        overlap = query_tokens & tokens

        if not overlap:
            continue

        score = len(overlap) / max(len(query_tokens), 1)

        results.append(
            {
                "document": path.name,
                "score": round(score, 4),
                "content": text,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:limit]
