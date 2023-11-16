from dataclasses import dataclass


@dataclass
class Book:
    name: str
    year: int
    rating: float
    link: str
