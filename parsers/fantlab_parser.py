import re
import uuid
from collections import Counter

import requests
from bs4 import BeautifulSoup

fantlab_url = "https://fantlab.ru"


class FantlabParser:
    @classmethod
    def search_books(cls, query: str):
        response = requests.get(
            f"{fantlab_url}/search-works",
            params={
                "q": query,
                'page': 'all'
            }
        )
        soup = BeautifulSoup(response.text, 'lxml')

        works_div = soup.select_one("div.works")

        if not works_div:
            return []

        counter = Counter([elem.text.strip() for elem in works_div.select("div.autor")])

        if len(counter) == 0 or counter.most_common(1)[0][0] != query:
            return []

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
            if book_type not in ['Цикл', 'Роман', 'Роман-эпопея', 'Повесть', 'Рассказ']:
                continue

            name = re.sub(r"\[.*]", "", book_title.split('/')[0]).strip()

            books.append({
                'name': name,
                'book_type': book_type,
                'year': int(parts[0] if len((parts := book_plus.split(', '))) > 1 else 0),
                'rating': float(big.text if (big := work_div.select_one("big")) else 0.0),
                'link': fantlab_url + work_div.select_one("div.title").a['href'],
                'uuid': str(uuid.uuid4())
            })

        return books

    @classmethod
    def get_book_translations(cls, book_url: str):
        result = []
        response = requests.get(book_url)
        soup = BeautifulSoup(response.text, 'lxml')

        translations_div = soup.select_one("#work-translations-unit")

        if not translations_div:
            return []

        for translate in translations_div.select("dd"):
            additional_info = re.findall(r'\d+', translate.find("span", attrs={"dir": "ltr"}).text)
            result.append({
                'persons': ",".join([person['title'] for person in translate.select("a.agray")]),
                'year': additional_info[0],
                'count': additional_info[1]
            })

        return result
