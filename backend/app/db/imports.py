# Import all SQLAlchemy models so Alembic can discover them through Base.metadata.
from app.models import (  # noqa: F401
    LoanApplication,
    LoanEligibilityRule,
    LoanProduct,
    Recommendation,
    RecommendationFactor,
    User,
    UserProfile,
)
