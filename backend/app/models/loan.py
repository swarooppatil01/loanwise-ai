from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import LoanType


class LoanProduct(Base):
    __tablename__ = "loan_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    lender: Mapped[str] = mapped_column(String(120), nullable=False)
    loan_type: Mapped[LoanType] = mapped_column(
        SAEnum(LoanType, name="loan_type"),
        nullable=False,
    )
    min_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    max_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    min_income: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    min_credit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_dti: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    min_interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    max_interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    min_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    max_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_fee_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    employment_types: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="salaried,self_employed",
    )
    special_conditions: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    rules = relationship(
        "LoanEligibilityRule",
        back_populates="loan_product",
        cascade="all, delete-orphan",
    )


class LoanEligibilityRule(Base):
    __tablename__ = "loan_eligibility_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_product_id: Mapped[int] = mapped_column(
        ForeignKey("loan_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rule_type: Mapped[str] = mapped_column(String(80), nullable=False)
    rule_value: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    loan_product = relationship("LoanProduct", back_populates="rules")
