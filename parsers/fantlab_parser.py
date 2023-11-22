import re
from collections import Counter
from typing import Optional

from bs4 import BeautifulSoup, Tag
from libs.sorter import orderby

from rapidfuzz import fuzz
from requests import get

from entities import Author, Book

fantlab_url = "https://fantlab.ru"


class FantlabParser:
    @classmethod
    def get_author_info(cls, query: str) -> Author | None:
        response = get(
            f"{fantlab_url}/search-works",
            params={
                "q": query,
                'page': 'all'
            }
        )
        soup = BeautifulSoup(response.text, 'lxml')

        if works_div := soup.select_one("div.works"):
            counter = Counter([elem.text.strip() for elem in works_div.select("div.autor")])

            if len(counter) == 0 or counter.most_common(1)[0][0] != query:
                return None

            author_name = counter.most_common(1)[0][0]

            books = []
            for work_div in works_div.select("div.one"):
                work_author = work_div.select_one("div.autor").text.strip()

                if work_author != author_name:
                    continue

                book_title = temp.text.strip() if (temp := work_div.select_one("div.title")) else ''
                book_plus = temp.text.strip() if (temp := work_div.select_one("div.plus")) else ''

                if not all([book_title, book_plus]):
                    continue

                book_type = book_plus.split(', ')[-1].capitalize()

                # TODO: Включить 'Поэма','Пьеса'.
                if book_type not in ['Роман', 'Роман-эпопея', 'Повесть', 'Рассказ']:
                    continue

                name = re.sub(r"\[.*]", "", book_title.split('/')[0]).strip()

                books.append(
                    Book(
                        name=name,
                        book_type=book_type,
                        year=int(parts[0] if len((parts := book_plus.split(', '))) > 1 else 0),
                        rating=float(big.text if (big := work_div.select_one("big")) else 0.0),
                        link=fantlab_url + work_div.select_one("div.title").a['href']
                    )
                )

            return Author(
                fullname=author_name,
                books=books
            )
        else:
            return None
