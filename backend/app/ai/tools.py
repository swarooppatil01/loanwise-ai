from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import LoanApplication, Recommendation
from app.models.loan import LoanProduct
from app.models.profile import UserProfile
from app.models.user import User


def get_user_profile(
    db: Session,
    user: User,
) -> dict:

    profile = db.scalar(
        select(UserProfile).where(
            UserProfile.user_id == user.id
        )
    )

    if profile is None:
        return {
            "found": False,
            "message": "The user has not completed their profile.",
        }

    return {
        "found": True,
        "age": profile.age,
        "city": profile.city,
        "employment_type": (
            profile.employment_type.value
            if profile.employment_type
            else None
        ),
        "currency": "INR",
        "currency_symbol": "₹",
        "monthly_income": (
            str(profile.monthly_income)
            if profile.monthly_income is not None
            else None
        ),
        "monthly_obligations": (
            str(profile.monthly_obligations)
            if profile.monthly_obligations is not None
            else None
        ),
        "credit_score": profile.credit_score,
        "employment_duration_months": (
            profile.employment_duration_months
        ),
    }


def get_available_loans(
    db: Session,
    loan_type: str | None = None,
) -> list[dict]:

    statement = select(LoanProduct).where(
        LoanProduct.is_active.is_(True)
    )

    if loan_type:
        statement = statement.where(
            LoanProduct.loan_type == loan_type
        )

    loans = db.scalars(
        statement.order_by(LoanProduct.id)
    ).all()

    return [
        {
            "id": loan.id,
            "name": loan.name,
            "lender": loan.lender,
            "loan_type": loan.loan_type.value,
            "currency": "INR",
            "currency_symbol": "₹",
            "min_amount": str(loan.min_amount),
            "max_amount": str(loan.max_amount),
            "min_income": str(loan.min_income),
            "min_credit_score": loan.min_credit_score,
            "max_dti": str(loan.max_dti),
            "min_interest_rate": str(loan.min_interest_rate),
            "max_interest_rate": str(loan.max_interest_rate),
            "min_tenure_months": loan.min_tenure_months,
            "max_tenure_months": loan.max_tenure_months,
            "processing_fee_percent": str(
                loan.processing_fee_percent
            ),
            "employment_types": loan.employment_types,
            "special_conditions": loan.special_conditions,
        }
        for loan in loans
    ]


def get_user_applications(
    db: Session,
    user: User,
) -> list[dict]:

    applications = db.scalars(
        select(LoanApplication)
        .where(
            LoanApplication.user_id == user.id
        )
        .order_by(
            LoanApplication.id.desc()
        )
    ).all()

    return [
        {
            "id": application.id,
            "loan_type": application.loan_type.value,
            "loan_amount": str(application.loan_amount),
            "currency": "INR",
            "currency_symbol": "₹",
            "preferred_tenure_months": (
                application.preferred_tenure_months
            ),
            "purpose": application.purpose,
            "status": application.status.value,
        }
        for application in applications
    ]


def get_application_recommendations(
    db: Session,
    user: User,
    application_id: int,
) -> dict:

    application = db.scalar(
        select(LoanApplication).where(
            LoanApplication.id == application_id,
            LoanApplication.user_id == user.id,
        )
    )

    if application is None:
        return {
            "found": False,
            "message": "Application not found.",
        }

    recommendations = db.scalars(
        select(Recommendation)
        .where(
            Recommendation.application_id == application.id
        )
        .order_by(
            Recommendation.rank
        )
    ).all()

    return {
        "found": True,
        "application": {
            "id": application.id,
            "loan_type": application.loan_type.value,
            "loan_amount": str(application.loan_amount),
            "currency": "INR",
            "currency_symbol": "₹",
            "preferred_tenure_months": (
                application.preferred_tenure_months
            ),
            "purpose": application.purpose,
            "status": application.status.value,
        },
        "recommendations": [
            {
                "id": recommendation.id,
                "loan_product_id": (
                    recommendation.loan_product_id
                ),
                "loan_name": (
                    recommendation.loan_product.name
                    if recommendation.loan_product
                    else None
                ),
                "score": str(recommendation.score),
                "rank": recommendation.rank,
                "eligible": recommendation.eligible,
                "explanation": recommendation.explanation,
                "factors": [
                    {
                        "factor": factor.factor,
                        "value": str(factor.value),
                        "weight": str(factor.weight),
                        "contribution": str(
                            factor.contribution
                        ),
                        "reason": factor.reason,
                    }
                    for factor in recommendation.factors
                ],
            }
            for recommendation in recommendations
        ],
    }


def search_loanwise_knowledge(
    query: str,
) -> dict:
    """
    Search the LoanWise knowledge base for general documentation,
    policies, methodology, and FAQ information.

    This knowledge base is NOT authoritative for current loan
    products, rates, fees, eligibility, availability, applications,
    or recommendation scores.
    """
    from app.rag.retriever import search_knowledge_base

    results = search_knowledge_base(
        query=query,
        limit=3,
    )

    return {
        "results": results,
    }
