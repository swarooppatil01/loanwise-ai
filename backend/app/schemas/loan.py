from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import LoanType


class LoanProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lender: str
    loan_type: LoanType
    min_amount: Decimal
    max_amount: Decimal
    min_income: Decimal
    min_credit_score: int
    max_dti: Decimal
    min_interest_rate: Decimal
    max_interest_rate: Decimal
    min_tenure_months: int
    max_tenure_months: int
    processing_fee_percent: Decimal
    employment_types: str
    special_conditions: str | None
    is_active: bool
