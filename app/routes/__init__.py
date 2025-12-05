# app/routes/__init__.py
from app.routes.stats import router as stats_router
from app.routes.verses import router as verses_router

__all__ = ["verses_router", "stats_router"]
