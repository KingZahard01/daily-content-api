import json
from typing import Any, Dict, List


# Cargar la Biblia completa
def load_bible() -> List[Dict[str, Any]]:
    """
    Carga la Biblia completa desde el archivo JSON.
    """
    try:
        with open("app/es_rvr.json", "r", encoding="utf-8-sig") as f:
            books = json.load(f)

        phrases = []

        for book in books:
            book_name = book["name"]
            for chapter_index, chapter in enumerate(book["chapters"], start=1):
                for verse_index, verse_text in enumerate(chapter, start=1):
                    phrases.append(
                        {
                            "text": verse_text,
                            "book": book_name,
                            "chapter": chapter_index,
                            "verse": verse_index,
                            "reference": f"{book_name} {chapter_index}:{verse_index}",
                            "version": "Reina Valera 1909",
                        }
                    )
        return phrases
    except FileNotFoundError:
        print("Error: Archivo de la Biblia no encontrado")
        return []
    except json.JSONDecodeError:
        print("Error: Archivo JSON inválido")
        return []


# Calcular estadísticas una vez al cargar
def calculate_stats(verses: List[Dict]) -> Dict[str, Any]:
    """
    Calcula estadísticas de la Biblia.
    """

    books = {}

    for verse in verses:
        book_name = verse["book"]
        if book_name not in books:
            books[book_name] = {"chapters": set(), "verses": 0}
        books[book_name]["chapters"].add(verse["chapter"])
        books[book_name]["verses"] += 1

    return books


VERSES = load_bible()
TOTAL_VERSES = len(VERSES)
BOOKS_STATS = calculate_stats(VERSES)
