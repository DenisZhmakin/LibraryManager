import re

from requests import get
from bs4 import BeautifulSoup, Tag

from entities import Author, Book
from .abstract_parser import AbstractParser

fantlab_url = "https://fantlab.ru"


class FantlabParser(AbstractParser):
    def get_authors(self, query: str):
        response = get(f"{fantlab_url}/searchmain", params={
            "searchstr": query
        })

        soup = BeautifulSoup(response.text, 'html.parser')

        if authors_div := soup.select_one("div.autors"):
            result = []
            for author_div in authors_div.select("div.one"):
                result.append(fantlab_url + author_div.a['href'])

            return result

        return False

    def get_author_info(self, url: str) -> Author:
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        def get_book_list(html: Tag) -> list[Book]:
            books = []

            if html is None:
                return books

            for item in html.findAll("tr", {"valign": "bottom"}):
                dots_div = item.select_one("div.dots")
                rating_span = item.find("span", id=re.compile(r"^m_"))

                books.append(Book(
                    name=dots_div.select_one("a").text.strip(),
                    year=int(dots_div.select_one("font").text),
                    rating=float(rating_span.text.split()[0] if rating_span else 'nan'),
                    link=fantlab_url + dots_div.select_one("a")['href']
                ))

            return books

        return Author(
            name=soup.find("h1", {'itemprop': 'name'}, recursive=True).text,
            country=soup.find("span", {'itemprop': 'nationality'}, recursive=True).text,
            novels=get_book_list(soup.select_one("#novel_info")),
            stories=get_book_list(soup.select_one("#story_info")),
            short_stories=get_book_list(soup.select_one("#shortstory_info"))
        )
