from decimal import Decimal

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.enums import LoanType
from app.models.loan import LoanProduct


LOANS = [
    {
        "name": "LoanWise Flex Personal",
        "lender": "LoanWise Demo Lender",
        "loan_type": LoanType.PERSONAL,
        "min_amount": Decimal("50000"),
        "max_amount": Decimal("1500000"),
        "min_income": Decimal("30000"),
        "min_credit_score": 650,
        "max_dti": Decimal("0.45"),
        "min_interest_rate": Decimal("11.00"),
        "max_interest_rate": Decimal("16.00"),
        "min_tenure_months": 12,
        "max_tenure_months": 60,
        "processing_fee_percent": Decimal("1.50"),
        "employment_types": "salaried,self_employed,professional",
        "special_conditions": "Demo product for the LoanWise AI technical project.",
    },
    {
        "name": "LoanWise Prime Personal",
        "lender": "LoanWise Demo Lender",
        "loan_type": LoanType.PERSONAL,
        "min_amount": Decimal("100000"),
        "max_amount": Decimal("2500000"),
        "min_income": Decimal("50000"),
        "min_credit_score": 720,
        "max_dti": Decimal("0.40"),
        "min_interest_rate": Decimal("9.50"),
        "max_interest_rate": Decimal("13.00"),
        "min_tenure_months": 12,
        "max_tenure_months": 72,
        "processing_fee_percent": Decimal("1.00"),
        "employment_types": "salaried,professional",
        "special_conditions": "Demo product for the LoanWise AI technical project.",
    },
    {
        "name": "LoanWise Self-Employed Flex",
        "lender": "LoanWise Demo Lender",
        "loan_type": LoanType.PERSONAL,
        "min_amount": Decimal("100000"),
        "max_amount": Decimal("1800000"),
        "min_income": Decimal("40000"),
        "min_credit_score": 680,
        "max_dti": Decimal("0.45"),
        "min_interest_rate": Decimal("11.50"),
        "max_interest_rate": Decimal("17.00"),
        "min_tenure_months": 12,
        "max_tenure_months": 60,
        "processing_fee_percent": Decimal("1.75"),
        "employment_types": "self_employed,business_owner,professional",
        "special_conditions": "Demo product; income documentation may be required.",
    },
]


def seed():
    with SessionLocal() as db:
        for payload in LOANS:
            exists = db.scalar(
                select(LoanProduct).where(LoanProduct.name == payload["name"])
            )
            if not exists:
                db.add(LoanProduct(**payload))

        db.commit()
        print(f"Seeded {len(LOANS)} demo loan products.")


if __name__ == "__main__":
    seed()
