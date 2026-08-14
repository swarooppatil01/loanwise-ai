from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.profile import UserProfile
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileUpsert

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse | None)
def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.scalar(select(UserProfile).where(UserProfile.user_id == current_user.id))


@router.put("", response_model=ProfileResponse)
def upsert_profile(
    payload: ProfileUpsert,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == current_user.id))

    if profile is None:
        profile = UserProfile(user_id=current_user.id, **payload.model_dump())
        db.add(profile)
    else:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
