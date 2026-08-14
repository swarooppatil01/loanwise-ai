from decimal import Decimal, ROUND_HALF_UP

from app.models.application import (
    LoanApplication,
    Recommendation,
    RecommendationFactor,
)
from app.models.loan import LoanProduct
from app.models.profile import UserProfile


WEIGHTS = {
    "credit_score": Decimal("0.25"),
    "dti": Decimal("0.25"),
    "income": Decimal("0.15"),
    "loan_amount": Decimal("0.15"),
    "tenure": Decimal("0.10"),
    "employment_type": Decimal("0.10"),
}


def clamp(value: Decimal) -> Decimal:
    return max(Decimal("0"), min(Decimal("1"), value))


def calculate_dti(profile: UserProfile) -> Decimal:
    if not profile.monthly_income or profile.monthly_income <= 0:
        return Decimal("1")

    return profile.monthly_obligations / profile.monthly_income


def score_credit(
    credit_score: int,
    minimum_credit_score: int,
) -> Decimal:
    if credit_score < minimum_credit_score:
        return Decimal("0")

    # Gives stronger scores to applicants comfortably above
    # the minimum required credit score.
    score = Decimal(credit_score - minimum_credit_score) / Decimal("180")
    return clamp(Decimal("0.60") + score * Decimal("0.40"))


def score_dti(
    dti: Decimal,
    maximum_dti: Decimal,
) -> Decimal:
    if dti > maximum_dti:
        return Decimal("0")

    if maximum_dti <= 0:
        return Decimal("0")

    return clamp(
        Decimal("1")
        - (dti / maximum_dti) * Decimal("0.50")
    )


def score_income(
    monthly_income: Decimal,
    minimum_income: Decimal,
) -> Decimal:
    if monthly_income < minimum_income:
        return Decimal("0")

    ratio = monthly_income / minimum_income

    if ratio >= Decimal("2"):
        return Decimal("1")

    return clamp(
        Decimal("0.50")
        + (ratio - Decimal("1")) * Decimal("0.50")
    )


def score_amount(
    requested_amount: Decimal,
    minimum_amount: Decimal,
    maximum_amount: Decimal,
) -> Decimal:
    if requested_amount < minimum_amount:
        return Decimal("0")

    if requested_amount > maximum_amount:
        return Decimal("0")

    available_range = maximum_amount - minimum_amount

    if available_range <= 0:
        return Decimal("1")

    # Prefer requests comfortably inside the supported amount range.
    midpoint = (minimum_amount + maximum_amount) / Decimal("2")

    if requested_amount <= midpoint:
        distance = requested_amount - minimum_amount
        return clamp(
            Decimal("0.70")
            + (distance / (midpoint - minimum_amount)) * Decimal("0.30")
            if midpoint > minimum_amount
            else Decimal("1")
        )

    distance = maximum_amount - requested_amount
    return clamp(
        Decimal("0.70")
        + (distance / (maximum_amount - midpoint)) * Decimal("0.30")
        if maximum_amount > midpoint
        else Decimal("1")
    )


def score_tenure(
    requested_tenure: int,
    minimum_tenure: int,
    maximum_tenure: int,
) -> Decimal:
    if requested_tenure < minimum_tenure:
        return Decimal("0")

    if requested_tenure > maximum_tenure:
        return Decimal("0")

    tenure_range = maximum_tenure - minimum_tenure

    if tenure_range <= 0:
        return Decimal("1")

    # Prefer moderate tenure rather than automatically rewarding
    # the longest possible repayment period.
    midpoint = minimum_tenure + tenure_range // 2

    distance = abs(requested_tenure - midpoint)
    maximum_distance = max(midpoint - minimum_tenure, maximum_tenure - midpoint)

    if maximum_distance == 0:
        return Decimal("1")

    return clamp(
        Decimal("1")
        - (Decimal(distance) / Decimal(maximum_distance)) * Decimal("0.30")
    )


def score_employment(
    employment_type: str | None,
    supported_types: str,
) -> Decimal:
    if not employment_type:
        return Decimal("0")

    supported = {
        item.strip().lower()
        for item in supported_types.split(",")
        if item.strip()
    }

    if employment_type.lower() in supported:
        return Decimal("1")

    return Decimal("0")


def round_decimal(value: Decimal, places: str = "0.001") -> Decimal:
    return value.quantize(
        Decimal(places),
        rounding=ROUND_HALF_UP,
    )


def build_recommendation(
    application: LoanApplication,
    profile: UserProfile,
    loan: LoanProduct,
) -> tuple[Recommendation, list[RecommendationFactor]]:
    dti = calculate_dti(profile)

    employment_type = (
        profile.employment_type.value
        if profile.employment_type
        else None
    )

    credit_value = score_credit(
        profile.credit_score or 0,
        loan.min_credit_score,
    )

    dti_value = score_dti(
        dti,
        loan.max_dti,
    )

    income_value = score_income(
        profile.monthly_income or Decimal("0"),
        loan.min_income,
    )

    amount_value = score_amount(
        application.loan_amount,
        loan.min_amount,
        loan.max_amount,
    )

    tenure_value = score_tenure(
        application.preferred_tenure_months,
        loan.min_tenure_months,
        loan.max_tenure_months,
    )

    employment_value = score_employment(
        employment_type,
        loan.employment_types,
    )

    eligible = all(
        [
            amount_value > 0,
            income_value > 0,
            credit_value > 0,
            dti <= loan.max_dti,
            tenure_value > 0,
            employment_value > 0,
            application.loan_type == loan.loan_type,
        ]
    )

    values = {
        "credit_score": credit_value,
        "dti": dti_value,
        "income": income_value,
        "loan_amount": amount_value,
        "tenure": tenure_value,
        "employment_type": employment_value,
    }

    score = sum(
        values[name] * WEIGHTS[name] * Decimal("100")
        for name in values
    )

    reasons = []

    if credit_value > 0:
        reasons.append(
            f"Credit score {profile.credit_score} meets the minimum "
            f"requirement of {loan.min_credit_score}."
        )
    else:
        reasons.append(
            f"Credit score {profile.credit_score} is below the "
            f"minimum requirement of {loan.min_credit_score}."
        )

    if dti <= loan.max_dti:
        reasons.append(
            f"DTI of {dti:.2%} is within the maximum allowed "
            f"{loan.max_dti:.2%}."
        )
    else:
        reasons.append(
            f"DTI of {dti:.2%} exceeds the maximum allowed "
            f"{loan.max_dti:.2%}."
        )

    if income_value > 0:
        reasons.append(
            f"Monthly income of ₹{profile.monthly_income:,.2f} "
            f"meets the minimum income requirement."
        )
    else:
        reasons.append(
            f"Monthly income is below the minimum requirement of "
            f"₹{loan.min_income:,.2f}."
        )

    if employment_value > 0:
        reasons.append(
            f"Employment type '{employment_type}' is supported."
        )
    else:
        reasons.append(
            f"Employment type '{employment_type}' is not supported."
        )

    recommendation = Recommendation(
        application_id=application.id,
        loan_product_id=loan.id,
        score=round_decimal(score),
        rank=0,
        eligible=eligible,
        explanation=" ".join(reasons),
    )

    factors = []

    for name, value in values.items():
        contribution = value * WEIGHTS[name] * Decimal("100")

        factors.append(
            RecommendationFactor(
                factor=name,
            value=round_decimal(value, "0.0001"),
                weight=round_decimal(WEIGHTS[name], "0.0001"),
                contribution=round_decimal(contribution, "0.0001"),
                reason=_factor_reason(
                    name=name,
                    value=value,
                    profile=profile,
                    loan=loan,
                    dti=dti,
                ),
            )
        )

    return recommendation, factors


def _factor_reason(
    name: str,
    value: Decimal,
    profile: UserProfile,
    loan: LoanProduct,
    dti: Decimal,
) -> str:
    if name == "credit_score":
        return (
            f"Applicant credit score: {profile.credit_score}; "
            f"minimum required: {loan.min_credit_score}."
        )

    if name == "dti":
        return (
            f"Applicant DTI: {dti:.2%}; "
            f"maximum allowed: {loan.max_dti:.2%}."
        )

    if name == "income":
        return (
            f"Applicant monthly income: ₹{profile.monthly_income:,.2f}; "
            f"minimum required: ₹{loan.min_income:,.2f}."
        )

    if name == "loan_amount":
        return (
            f"Requested amount: ₹{loan.min_amount:,.2f}–"
            f"₹{loan.max_amount:,.2f} supported."
        )

    if name == "tenure":
        return (
            f"Requested loan tenure: {loan.min_tenure_months}–{loan.max_tenure_months} "
            f"months supported."
        )

    if name == "employment_type":
        employment = (
            profile.employment_type.value
            if profile.employment_type
            else "unknown"
        )
        return (
            f"Applicant employment type: {employment}; "
            f"supported types: {loan.employment_types}."
        )

    return f"{name} contributes to the recommendation score."
