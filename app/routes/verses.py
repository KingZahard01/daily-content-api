from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models import (
    DailyVerseResponse,
    ErrorResponse,
    VerseResponse,
    VersesListResponse,
)
from app.services import VerseService

router = APIRouter(prefix="/api", tags=["Versículos"])


@router.get("/daily-verse", response_model=DailyVerseResponse)
def daily_verse():
    """
    Devuelve un versículo diferente cada día.
    """
    verse = VerseService.get_daily_verse()
    return {"date": str(date.today()), **verse}


@router.get("/random-verse", response_model=VerseResponse)
def random_verse():
    """
    Devuelve un versículo aleatorio.
    """
    verse = VerseService.get_random_verse()
    return verse


@router.get("/verses", response_model=VersesListResponse)
def get_verses(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    book: Optional[str] = Query(None),
    chapter: Optional[int] = Query(None, ge=1),
):
    """
    Devuelve versículos con paginación y filtros.
    """
    verses, total = VerseService.get_verses(book, chapter, limit, offset)

    return {
        "total": total,
        "returned": len(verses),
        "limit": limit,
        "offset": offset,
        "filters": {"book": book, "chapter": chapter},
        "verses": verses,
    }


@router.get(
    "/verse/{book}/{chapter}/{verse_number}",
    response_model=VerseResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_specific_verse(book: str, chapter: int, verse_number: int):
    """
    Obtiene un versículo específico.
    """
    verse = VerseService.get_specific_verse(book, chapter, verse_number)
    if not verse:
        raise HTTPException(
            status_code=404,
            detail=f"Versículo no encontrado: {book} {chapter}:{verse_number}",
        )
    return verse
