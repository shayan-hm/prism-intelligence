"""Root API router."""

from fastapi import APIRouter

from prism.interfaces.api.health import router as health_router
from prism.infrastructure.config import get_settings


api_router = APIRouter()


@api_router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
        "status": "ok",
    }


# Health check router (no prefix)
api_router.include_router(health_router)

# Future v1 routers - uncomment when implemented
# from prism.interfaces.api.v1.market import router as market_router
# from prism.interfaces.api.v1.portfolio import router as portfolio_router
# from prism.interfaces.api.v1.risk import router as risk_router
#
# api_router.include_router(market_router, prefix="/market", tags=["market"])
# api_router.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
# api_router.include_router(risk_router, prefix="/risk", tags=["risk"])