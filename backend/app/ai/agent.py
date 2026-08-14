from typing import Any

from sqlalchemy.orm import Session

from app.ai.gemini import get_gemini_client
from app.ai.exceptions import AIProviderError
from app.ai.prompts import SYSTEM_PROMPT
from app.ai.rag_tools import search_loanwise_knowledge
from app.ai.tools import (
    get_application_recommendations,
    get_available_loans,
    get_user_applications,
    get_user_profile,
)
from app.core.config import settings
from app.models.user import User


def build_tools(
    db: Session,
    user: User,
) -> list[Any]:
    """
    Build authenticated LoanWise tools for the current user.

    These functions close over the authenticated database session
    and user, so Gemini never receives direct database access.
    """

    def get_my_profile() -> dict:
        """
        Get the authenticated user's LoanWise financial profile.

        Use this when the user asks about their income, credit score,
        employment, obligations, city, age, or other profile details.
        """
        return get_user_profile(
            db,
            user,
        )

    def get_available_loan_products(
        loan_type: str | None = None,
    ) -> dict:
        """
        Get currently active LoanWise loan products.

        Optionally filter by loan type:
        personal, home, education, or vehicle.
        """
        return {
            "loans": get_available_loans(
                db,
                loan_type,
            )
        }

    def get_my_applications() -> dict:
        """
        Get all loan applications belonging to the authenticated user.
        """
        return {
            "applications": get_user_applications(
                db,
                user,
            )
        }

    def get_my_recommendations(
        application_id: int,
    ) -> dict:
        """
        Get the authoritative LoanWise recommendation results
        for one of the authenticated user's applications.

        Never use this to make an independent eligibility decision.
        """
        return get_application_recommendations(
            db,
            user,
            application_id,
        )

    return [
        get_my_profile,
        get_available_loan_products,
        get_my_applications,
        get_my_recommendations,
        search_loanwise_knowledge,
    ]


def run_agent(
    message: str,
    db: Session,
    user: User,
    application_id: int | None = None,
) -> str:
    """
    Run the LoanWise Gemini assistant for the authenticated user.
    """

    client = get_gemini_client()

    tools = build_tools(
        db,
        user,
    )

    user_message = message.strip()

    if application_id is not None:
        user_message += (
            f"\n\nThe current LoanWise application ID is "
            f"{application_id}. Use the application-specific "
            f"tool when answering questions about this application."
        )

    chat = client.chats.create(
        model=settings.ai_model,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "tools": tools,
        },
    )

    try:
        response = chat.send_message(
            user_message
        )
    except Exception as exc:
        raise AIProviderError(
            "Gemini provider request failed."
        ) from exc

    answer = getattr(response, "text", None)

    if answer:
        return answer.strip()

    return (
        "I couldn't generate a response right now. "
        "Please try again."
    )
