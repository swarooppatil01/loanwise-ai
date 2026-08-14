from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ApplicationStatus, LoanType
from app.schemas.loan import LoanProductResponse


class LoanApplicationCreate(BaseModel):
    loan_type: LoanType
    loan_amount: Decimal = Field(gt=0)
    preferred_tenure_months: int = Field(gt=0, le=600)
    purpose: str = Field(min_length=3, max_length=500)


class RecommendationFactorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    factor: str
    value: Decimal
    weight: Decimal
    contribution: Decimal
    reason: str


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    loan_product_id: int
    score: Decimal
    rank: int
    eligible: bool
    explanation: str | None
    loan_product: LoanProductResponse
    factors: list[RecommendationFactorResponse]


class LoanApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    loan_type: LoanType
    loan_amount: Decimal
    preferred_tenure_months: int
    purpose: str
    status: ApplicationStatus
    recommendations: list[RecommendationResponse] = Field(default_factory=list)
