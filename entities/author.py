from dataclasses import dataclass, field
from typing import Optional

from .book import Book


@dataclass
class Author:
    name: str
    books: list[Book] = field(default_factory=list)
