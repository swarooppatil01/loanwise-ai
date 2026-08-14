from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EmploymentType


class ProfileUpsert(BaseModel):
    age: int | None = Field(default=None, ge=18, le=100)
    city: str | None = Field(default=None, max_length=100)
    employment_type: EmploymentType | None = None
    monthly_income: Decimal | None = Field(default=None, ge=0)
    monthly_obligations: Decimal | None = Field(default=None, ge=0)
    credit_score: int | None = Field(default=None, ge=300, le=900)
    employment_duration_months: int | None = Field(default=None, ge=0, le=600)


class ProfileResponse(ProfileUpsert):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
