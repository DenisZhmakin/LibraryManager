from abc import ABC, abstractmethod

from entities import Author


class AbstractParser(ABC):
    @abstractmethod
    def get_authors(self, query: str):
        pass

    @abstractmethod
    def get_author_info(self, url: str) -> Author:
        pass
