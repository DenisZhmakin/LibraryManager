import re
from typing import Union, Tuple

import requests
from bs4 import BeautifulSoup, Tag

from dataclasses import dataclass, field

from utils import get_book_type


@dataclass
class Book:
    title: str
    author: str
    book_type: str
    writing_year: Union[int, Tuple[int, int]]

    alternative_titles: list[str] = field(default_factory=list)

    @classmethod
    def extract_data_from_url(cls, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        general_info = soup.select_one("div#work-names-unit")

        alternative_titles_tag = general_info.find("p", text=re.compile("^Другие названия:"))

        if alternative_titles_tag:
            alternative_titles_raw = alternative_titles_tag.text.replace("Другие названия:", "").strip()
            alternative_titles = [alt_title.strip() for alt_title in alternative_titles_raw.split(';')]
        else:
            alternative_titles = []

        date_published_tag = general_info.select_one('span[itemprop="datePublished"]')

        return cls(
            title=general_info.select_one('span[itemprop="name"]').text.strip(),
            author=general_info.select_one('a[itemprop="author"]').text.strip(),
            writing_year=int(date_published_tag.text.strip()) if date_published_tag else 0,
            alternative_titles=alternative_titles,
            book_type=get_book_type(general_info),
        )
