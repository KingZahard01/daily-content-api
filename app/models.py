from typing import List  # , Optional

from pydantic import BaseModel


class VerseBase(BaseModel):
    text: str
    book: str
    chapter: int
    verse: int
    reference: str
    version: str


class VerseResponse(VerseBase):
    pass


class DailyVerseResponse(VerseResponse):
    date: str


class VersesListResponse(BaseModel):
    total: int
    returned: int
    limit: int
    offset: int
    filters: dict
    verses: List[VerseResponse]


class BookStats(BaseModel):
    name: str
    chapters: int
    verses: int


class StatsResponse(BaseModel):
    total_verses: int
    total_books: int
    books: List[BookStats]


class ErrorResponse(BaseModel):
    detail: str
