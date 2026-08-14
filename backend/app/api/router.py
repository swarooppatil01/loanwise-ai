from fastapi import APIRouter

from app.api import ai, applications, auth, health, loans, profile

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(loans.router)

api_router.include_router(applications.router)

api_router.include_router(ai.router)
