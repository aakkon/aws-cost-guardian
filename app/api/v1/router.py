from fastapi import APIRouter
from app.api.v1 import health, costs

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(costs.router, prefix="", tags=["costs"])
