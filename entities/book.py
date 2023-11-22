from dataclasses import dataclass


@dataclass
class Book:
    name: str
    book_type: str
    year: int
    rating: float
    link: str
