from dataclasses import dataclass, field

from .book import Book


@dataclass
class Author:
    name: str
    country: str
    novels: list[Book] = field(default_factory=list)
    stories: list[Book] = field(default_factory=list)
    short_stories: list[Book] = field(default_factory=list)
    genres: list[str] = field(default_factory=list)
