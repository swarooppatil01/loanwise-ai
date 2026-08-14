from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ApplicationStatus, LoanType


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    loan_type: Mapped[LoanType] = mapped_column(
        SAEnum(LoanType, name="application_loan_type"),
        nullable=False,
    )
    loan_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    preferred_tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        SAEnum(ApplicationStatus, name="application_status"),
        default=ApplicationStatus.DRAFT,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship("User", back_populates="applications")
    recommendations = relationship(
        "Recommendation",
        back_populates="application",
        cascade="all, delete-orphan",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    loan_product_id: Mapped[int] = mapped_column(
        ForeignKey("loan_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[Decimal] = mapped_column(Numeric(6, 3), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    eligible: Mapped[bool] = mapped_column(nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    application = relationship("LoanApplication", back_populates="recommendations")
    loan_product = relationship("LoanProduct")
    factors = relationship(
        "RecommendationFactor",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )


class RecommendationFactor(Base):
    __tablename__ = "recommendation_factors"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey("recommendations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    factor: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    contribution: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    recommendation = relationship("Recommendation", back_populates="factors")
