from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.application import LoanApplication, Recommendation
from app.models.enums import ApplicationStatus
from app.models.loan import LoanProduct
from app.models.profile import UserProfile
from app.models.user import User
from app.schemas.application import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    RecommendationResponse,
)
from app.services.recommendation import build_recommendation


router = APIRouter(prefix="/applications", tags=["Loan Applications"])


@router.post(
    "",
    response_model=LoanApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: LoanApplicationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    profile = db.scalar(
        select(UserProfile).where(
            UserProfile.user_id == current_user.id
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete your profile before applying for a loan.",
        )

    if profile.monthly_income is None or profile.monthly_income <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monthly income is required before applying for a loan.",
        )

    if profile.credit_score is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit score is required before applying for a loan.",
        )

    application = LoanApplication(
        user_id=current_user.id,
        loan_type=payload.loan_type,
        loan_amount=payload.loan_amount,
        preferred_tenure_months=payload.preferred_tenure_months,
        purpose=payload.purpose,
        status=ApplicationStatus.SUBMITTED,
    )

    db.add(application)
    db.flush()

    loans = list(
        db.scalars(
            select(LoanProduct)
            .where(
                LoanProduct.is_active.is_(True),
                LoanProduct.loan_type == payload.loan_type,
            )
            .order_by(LoanProduct.id)
        ).all()
    )

    if not loans:
        application.status = ApplicationStatus.FAILED
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active loan products are available for this loan type.",
        )

    recommendations = []

    for loan in loans:
        recommendation, factors = build_recommendation(
            application=application,
            profile=profile,
            loan=loan,
        )

        recommendation.factors = factors
        recommendations.append(recommendation)

    recommendations.sort(
        key=lambda item: (item.eligible, item.score),
        reverse=True,
    )

    for rank, recommendation in enumerate(recommendations, start=1):
        recommendation.rank = rank
        db.add(recommendation)

    application.status = ApplicationStatus.PROCESSED

    db.commit()

    application = db.scalar(
        select(LoanApplication)
        .options(
            selectinload(LoanApplication.recommendations)
            .selectinload(Recommendation.loan_product),
            selectinload(LoanApplication.recommendations)
            .selectinload(Recommendation.factors),
        )
        .where(LoanApplication.id == application.id)
    )

    return application


@router.get(
    "",
    response_model=list[LoanApplicationResponse],
)
def get_applications(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    applications = list(
        db.scalars(
            select(LoanApplication)
            .options(
                selectinload(LoanApplication.recommendations)
                .selectinload(Recommendation.loan_product),
                selectinload(LoanApplication.recommendations)
                .selectinload(Recommendation.factors),
            )
            .where(
                LoanApplication.user_id == current_user.id,
            )
            .order_by(LoanApplication.created_at.desc())
        ).all()
    )

    return applications


@router.get(
    "/{application_id}",
    response_model=LoanApplicationResponse,
)
def get_application(
    application_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    application = db.scalar(
        select(LoanApplication)
        .options(
            selectinload(LoanApplication.recommendations)
            .selectinload(Recommendation.loan_product),
            selectinload(LoanApplication.recommendations)
            .selectinload(Recommendation.factors),
        )
        .where(
            LoanApplication.id == application_id,
            LoanApplication.user_id == current_user.id,
        )
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan application not found.",
        )

    return application


@router.get(
    "/{application_id}/recommendations",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    application_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    application = db.scalar(
        select(LoanApplication).where(
            LoanApplication.id == application_id,
            LoanApplication.user_id == current_user.id,
        )
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan application not found.",
        )

    return list(
        db.scalars(
            select(Recommendation)
            .options(
                selectinload(Recommendation.loan_product),
                selectinload(Recommendation.factors),
            )
            .where(
                Recommendation.application_id == application_id
            )
            .order_by(Recommendation.rank)
        ).all()
    )
