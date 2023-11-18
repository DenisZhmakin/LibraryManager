from dataclasses import dataclass


@dataclass
class Book:
    name: str
    type: str
    year: int
    rating: float
    link: str
