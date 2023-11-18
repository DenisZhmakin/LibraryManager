import re
from collections import Counter
from typing import Optional

from requests import get
from bs4 import BeautifulSoup, Tag
from fuzzywuzzy import process as fuzz_process

from entities import Author, Book
from .abstract_parser import AbstractParser

fantlab_url = "https://fantlab.ru"


class FantlabParser(AbstractParser):
    def get_author_info(self, query: str) -> Optional[Author]:
        response = get(f"{fantlab_url}/searchmain", params={"searchstr": query})
        soup = BeautifulSoup(response.text, 'lxml')

        def get_book_list(html: Tag, book_t: str) -> list[Book]:
            books = []

            if html is None:
                return books

            for item in html.findAll("tr", {"valign": "bottom"}):
                dots_div = item.select_one("div.dots")
                rating_span = item.find("span", id=re.compile(r"^m_"))

                book_info = dots_div.find("a", {"title": None}, recursive=True)

                books.append(Book(
                    type=book_t,
                    name=book_info.text.strip(),
                    year=int(font.text if (font := dots_div.select_one("font")) else 0),
                    rating=float(rating_span.text.split()[0] if rating_span else 0.0),
                    link=fantlab_url + book_info['href']
                ))

            return books

        if authors_div := soup.select_one("div.autors"):
            authors = [
                {
                    'name': div.select_one("div.title").select_one("a").text,
                    'href': fantlab_url + div.a['href']
                } for div in authors_div.select("div.one")
            ]

            author = fuzz_process.extractOne(query, authors)

            response = get(author[0]['href'])
            soup = BeautifulSoup(response.text, 'lxml')

            author_books = get_book_list(soup.select_one("tbody#novel_info"), 'Роман')
            author_books.extend(get_book_list(soup.select_one("#story_info"), 'Повесть')),
            author_books.extend(get_book_list(soup.select_one("#shortstory_info"), 'Рассказ'))

            return Author(
                name=soup.find("h1", {'itemprop': 'name'}, recursive=True).text,
                books=author_books
            )
        else:
            response = get(f"{fantlab_url}/search-works", params={
                "q": query,
                'page': 'all'
            })
            soup = BeautifulSoup(response.text, 'lxml')

            works_div = soup.select_one("div.works")

            if not works_div:
                return None

            counter = Counter([elem.text.strip() for elem in works_div.select("div.autor")])

            if len(counter) == 0:
                return None

            author_name = counter.most_common(1)[0][0]

            author = Author(name=author_name)

            for work_div in works_div.select("div.one"):
                work_author = work_div.select_one("div.autor").text.strip()

                if work_author != author_name:
                    continue

                book_title = temp.text.strip() if (temp := work_div.select_one("div.title")) else ''
                book_plus = temp.text.strip() if (temp := work_div.select_one("div.plus")) else ''

                if not all([book_title, book_plus]):
                    continue

                book_type = book_plus.split(', ')[-1].capitalize()

                # TODO: Включить 'Цикл','Поэма','Пьеса'.
                if book_type not in ['Роман', 'Повесть', 'Рассказ']:
                    continue

                author.books.append(
                    Book(
                        name=book_title.split('/')[0],
                        type=book_type,
                        year=int(parts[0] if len((parts := book_plus.split(', '))) > 1 else 0),
                        rating=float(big.text if (big := work_div.select_one("big")) else 0.0),
                        link=fantlab_url + work_div.select_one("div.title").a['href']
                    )
                )

            return author
