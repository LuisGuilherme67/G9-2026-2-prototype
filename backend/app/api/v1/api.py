from fastapi import APIRouter
from app.api.v1.routers import auth, cadeiras, analytics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(cadeiras.router)
api_router.include_router(analytics.router)
