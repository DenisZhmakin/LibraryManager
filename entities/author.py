from dataclasses import dataclass, field
from typing import Optional

from .book import Book


@dataclass
class Author:
    fullname: str
    books: list[Book] = field(default_factory=list)

    is_duet: bool = False
    names: list[str] = field(default_factory=list)

    surname: str = None
    name: Optional[str] = None
    patronymic: Optional[str] = None

    def __post_init__(self):
        parts = list(filter(lambda x: len(x) > 1, self.fullname.split()))

        if len(parts) == 2:
            self.is_duet = False
            self.name = parts[0]
            self.surname = parts[-1]
        elif len(parts) >= 3 and 'и' not in self.fullname.split():
            self.is_duet = False
            self.name = parts[0]
            self.surname = parts[-1]
            self.patronymic = parts[1]
        else:
            self.is_duet = True
            self.surname = parts[-1][0:-1]
            self.names = parts[0:-1]
