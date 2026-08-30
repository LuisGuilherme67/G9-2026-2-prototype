"""Pacote de Rotas HTTP da API v1."""
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.cadeiras import router as cadeiras_router
from app.api.v1.routers.analytics import router as analytics_router

__all__ = ["auth_router", "cadeiras_router", "analytics_router"]
