from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.agent import run_agent
from app.ai.schemas import AIChatRequest, AIChatResponse
from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat(
    payload: AIChatRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        answer = run_agent(
            message=payload.message,
            db=db,
            user=current_user,
            application_id=payload.application_id,
        )

        return AIChatResponse(
            answer=answer,
            application_id=payload.application_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "LoanWise AI is temporarily unavailable. "
                "Please try again shortly."
            ),
        )
