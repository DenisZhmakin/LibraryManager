import re
from typing import Optional

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
    def find_writer_by_query(cls, query: str):
        session = cls._get_tor_session()

        response = session.get(
            url=f"{flibusta_url}/booksearch",
            params={
                'ask': query,
                'cha': 'on'
            }
        )

        soup = BeautifulSoup(response.text, 'lxml')

        for elem in soup.select('a[href^="/a/"]'):
            if elem.parent.name != 'li':
                continue

            return {
                'fio': elem.text.strip()
            }

    @classmethod
    def get_book_translations(cls, book_url):
        session = cls._get_tor_session()
        response = session.get(url=book_url)
        soup = BeautifulSoup(response.text, 'lxml')

        data_raw = re.search(r'\(перевод:.*\)', soup.text)

        if not data_raw:
            return []

        translations = []
        for tr in data_raw.group(0).replace('(перевод: ', '').replace(')', '').split(','):
            translations.append(tr.strip().split()[-1])

        return sorted(translations)

    @classmethod
    def get_book_variant(cls, author_surname: str, book_name: str, translators: Optional[dict] = None):
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
            book_url = flibusta_url + book_div.select_one('a[href^="/b/"]')['href']
            translations = cls.get_book_translations(book_url)

            books.append({
                'name': book_name,
                'size': book_div.find("span", {"style": "size"}).text,
                'translators': translations,
                'ratio': fuzz.WRatio(book_name, book_div.find("a", href=re.compile(r'^/b/\d*$')).text),
                'rating': RATING.get(book_div.find("img")['title']),
                'link': book_url,
                'order': index
            })

        books = sorted(books, key=orderby('rating ASC, ratio ASC, order DESC'), reverse=True)

        if translators:
            for book in books:
                if book['translators'] == translators['translators']:
                    return book
            else:
                return books[0]
        else:
            return books[0]
