import random
from datetime import date
from typing import Dict, List, Optional

from app.database import TOTAL_VERSES, VERSES


class VerseService:
    @staticmethod
    def get_daily_verse() -> Dict:
        """
        Obtiene el versiculo del dia basado en la fecha.
        """
        index = date.today().toordinal() % TOTAL_VERSES
        return VERSES[index]

    @staticmethod
    def get_random_verse() -> Dict:
        """
        Obtiene un versiculo aleatorio.
        """
        return random.choice(VERSES)

    @staticmethod
    def get_verses(
        book: Optional[str] = None,
        chapter: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[Dict], int]:
        """
        Filtra y pagína versículos.
        """
        filtered = VERSES

        if book:
            filtered = [v for v in filtered if v["book"].lower() == book.lower()]

        if chapter:
            filtered = [v for v in filtered if v["chapter"] == chapter]

        total = len(filtered)
        paginated = filtered[offset : offset + limit]

        return paginated, total

    @staticmethod
    def get_specific_verse(
        book: str, chapter: int, verse_number: int
    ) -> Optional[Dict]:
        """
        Busca un versiculo específico
        """
        for verse in VERSES:
            if (
                verse["book"].lower() == book.lower()
                and verse["chapter"] == chapter
                and verse["verse"] == verse_number
            ):
                return verse
        return None


class StatsService:
    @staticmethod
    def get_stats():
        """
        Genera estadisticas generales
        """
        from app.database import BOOKS_STATS, TOTAL_VERSES

        books_list = [
            {
                "name": book_name,
                "chapters": len(data["chapters"]),
                "verses": data["verses"],
            }
            for book_name, data in BOOKS_STATS.items()
        ]

        return {
            "total_verses": TOTAL_VERSES,
            "total_books": len(BOOKS_STATS),
            "books": books_list,
        }
