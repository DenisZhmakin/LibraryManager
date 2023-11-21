import re

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

from libs.sorter import orderby

flibusta_url = "http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion"

RATING = {
    'файл на 1': -3,
    'файл на 2': -2,
    'файл на 3': -1,
    'файл не оценен': 0,
    'файл на 4': 1,
    'файл на 5': 2
}


class FlibustaParser:
    @classmethod
    def _get_tor_session(cls):
        session = requests.session()

        session.proxies = {'http': 'socks5h://127.0.0.1:9150',
                           'https': 'socks5h://127.0.0.1:9150'}
        return session

    @classmethod
    def get_books(cls, author_surname: str, book_name: str):
        session = cls._get_tor_session()

        response = session.get(
            url=f"{flibusta_url}/makebooklist",
            params={
                'ab': 'ab1',
                'sort': 'sd2',
                't': book_name,
                'ln': author_surname,
                'e': 'fb2'
            }
        )

        soup = BeautifulSoup(response.text, 'lxml')

        books_form = soup.select_one("form[name='bk']")

        if not books_form:
            return None

        books = []
        for index, book_div in enumerate(books_form.findAll("div"), 1):
            books.append({
                'name': book_name,
                'size': book_div.find("span", {"style": "size"}).text,
                'ratio': fuzz.WRatio(book_name, book_div.find("a", href=re.compile(r'^/b/\d*$')).text),
                'rating': RATING.get(book_div.find("img")['title']),
                'link': flibusta_url + book_div.find("a", href=re.compile(r'fb2$'))['href'],
                'order': index
            })

        books = sorted(books, key=orderby('rating ASC, ratio ASC, order DESC'), reverse=True)

        if len(books) == 0:
            return None

        return books[0]
