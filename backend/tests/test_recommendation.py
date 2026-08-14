from decimal import Decimal

from app.models.enums import EmploymentType, LoanType
from app.models.loan import LoanProduct
from app.models.profile import UserProfile
from app.models.application import LoanApplication
from app.services.recommendation import (
    build_recommendation,
    calculate_dti,
)


def make_profile(
    income=Decimal("75000"),
    obligations=Decimal("10000"),
    credit_score=760,
    employment=EmploymentType.SALARIED,
):
    return UserProfile(
        user_id=1,
        age=23,
        city="Pune",
        employment_type=employment,
        monthly_income=income,
        monthly_obligations=obligations,
        credit_score=credit_score,
        employment_duration_months=24,
    )


def make_loan():
    return LoanProduct(
        id=1,
        name="Test Personal Loan",
        lender="Test Lender",
        loan_type=LoanType.PERSONAL,
        min_amount=Decimal("50000"),
        max_amount=Decimal("1500000"),
        min_income=Decimal("30000"),
        min_credit_score=650,
        max_dti=Decimal("0.45"),
        min_interest_rate=Decimal("11.00"),
        max_interest_rate=Decimal("16.00"),
        min_tenure_months=12,
        max_tenure_months=60,
        processing_fee_percent=Decimal("1.50"),
        employment_types="salaried,self_employed,professional",
        special_conditions="Test",
        is_active=True,
    )


def make_application():
    return LoanApplication(
        id=1,
        user_id=1,
        loan_type=LoanType.PERSONAL,
        loan_amount=Decimal("500000"),
        preferred_tenure_months=36,
        purpose="Testing",
    )


def test_dti_calculation():
    profile = make_profile()

    assert calculate_dti(profile) == Decimal("10000") / Decimal("75000")


def test_eligible_applicant():
    recommendation, factors = build_recommendation(
        make_application(),
        make_profile(),
        make_loan(),
    )

    assert recommendation.eligible is True
    assert recommendation.score > 0
    assert len(factors) == 6


def test_low_credit_score_is_ineligible():
    recommendation, _ = build_recommendation(
        make_application(),
        make_profile(credit_score=600),
        make_loan(),
    )

    assert recommendation.eligible is False


def test_high_dti_is_ineligible():
    recommendation, _ = build_recommendation(
        make_application(),
        make_profile(
            income=Decimal("50000"),
            obligations=Decimal("30000"),
        ),
        make_loan(),
    )

    assert recommendation.eligible is False


def test_unsupported_employment_type_is_ineligible():
    recommendation, _ = build_recommendation(
        make_application(),
        make_profile(
            employment=EmploymentType.BUSINESS_OWNER,
        ),
        make_loan(),
    )

    assert recommendation.eligible is False


def test_loan_amount_outside_range_is_ineligible():
    application = make_application()
    application.loan_amount = Decimal("3000000")

    recommendation, _ = build_recommendation(
        application,
        make_profile(),
        make_loan(),
    )

    assert recommendation.eligible is False


def test_tenure_outside_range_is_ineligible():
    application = make_application()
    application.preferred_tenure_months = 120

    recommendation, _ = build_recommendation(
        application,
        make_profile(),
        make_loan(),
    )

    assert recommendation.eligible is False
