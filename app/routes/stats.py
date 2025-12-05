from fastapi import APIRouter

from app.models import StatsResponse
from app.services import StatsService

router = APIRouter(prefix="/api", tags=["Estadísticas"])


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """
    Devuelve estadísticas completas de la Biblia.

    Incluye:
    - Total de versículos
    - Total de libros
    - Lista de libros con sus capítulos y versículos
    """
    stats = StatsService.get_stats()
    return stats
