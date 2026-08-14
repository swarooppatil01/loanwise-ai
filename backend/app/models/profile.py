from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import EmploymentType


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    age: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str | None] = mapped_column(String(100))
    employment_type: Mapped[EmploymentType | None] = mapped_column(
        SAEnum(EmploymentType, name="employment_type")
    )
    monthly_income: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    monthly_obligations: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    credit_score: Mapped[int | None] = mapped_column(Integer)
    employment_duration_months: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship("User", back_populates="profile")
