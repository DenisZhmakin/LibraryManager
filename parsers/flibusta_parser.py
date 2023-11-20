import re
import uuid

import requests
from bs4 import BeautifulSoup

flibusta_url = "http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion"


class FlibustaParser:
    @classmethod
    def _get_tor_session(cls):
        session = requests.session()

        session.proxies = {'http': 'socks5h://127.0.0.1:9150',
                           'https': 'socks5h://127.0.0.1:9150'}
        return session

    @classmethod
    def get_book_info(cls, author_surname: str, book_name: str):
        session = cls._get_tor_session()

        response = session.get(
            url=f"{flibusta_url}/makebooklist",
            params={
                'ab': 'ab1',
                't': book_name,
                'ln': author_surname,
                'e': 'fb2'
            }
        )

        soup = BeautifulSoup(response.text, 'lxml')

        books_form = soup.select_one("form[name='bk']")

        for book in books_form.findAll("div"):
            response = session.get(flibusta_url + book.find('a', href=re.compile(r'fb2$'))['href'],
                                   allow_redirects=True)

            with open(f'{uuid.uuid4().hex}.zip', 'wb') as f:
                f.write(response.content)

            print(flibusta_url + book.find('a', href=re.compile(r'fb2$'))['href'])
