from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enums import LoanType
from app.models.loan import LoanProduct
from app.schemas.loan import LoanProductResponse

router = APIRouter(prefix="/loans", tags=["Loan Products"])


@router.get("", response_model=list[LoanProductResponse])
def list_loans(
    db: Annotated[Session, Depends(get_db)],
    loan_type: LoanType | None = Query(default=None),
):
    statement = select(LoanProduct).where(LoanProduct.is_active.is_(True))

    if loan_type is not None:
        statement = statement.where(LoanProduct.loan_type == loan_type)

    return list(db.scalars(statement.order_by(LoanProduct.id)).all())


@router.get("/{loan_id}", response_model=LoanProductResponse)
def get_loan(
    loan_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    loan = db.scalar(
        select(LoanProduct).where(
            LoanProduct.id == loan_id,
            LoanProduct.is_active.is_(True),
        )
    )

    if loan is None:
        raise HTTPException(status_code=404, detail="Loan product not found")

    return loan
