import webbrowser

import flet as ft
from flet_core.dropdown import Option
from repath import match

from parsers import FantlabParser


class BookView(ft.View):
    def __init__(self, page: ft.Page, route: str):
        super().__init__(route=route)
        self.page = page
        book_uuid = match('/book/:uuid', page.route).groupdict()['uuid']

        book_info = list(filter(lambda b: b['uuid'] == book_uuid, self.page.client_storage.get("books")))[0]

        translations = FantlabParser.get_book_translations(book_info['link'])

        self.controls = [
            ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        margin=0,
                        width=float("inf"),
                        height=float("inf"),
                        expand=True
                    ),
                    ft.Container(
                        margin=ft.margin.only(left=30, top=0, right=0, bottom=0),
                        width=float("inf"),
                        height=float("inf"),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Text(f"Автор: {self.page.client_storage.get('author')}"),
                                ft.Text(f"Название: {book_info['name']}"),
                                ft.Text(f"Тип произведения: {book_info['book_type']}"),
                                ft.Text(f"Год написания: {book_info['year']}"),
                                ft.Text(f"Рейтинг: {book_info['rating']}"),
                                ft.Dropdown(
                                    label="Перевод",
                                    hint_text="Выберите перевод произведения",
                                    options=[
                                        Option(f"{tr['persons']} ({tr['year']} года), {tr['count']} изданий")
                                        for tr in translations
                                    ],
                                    autofocus=True
                                ),
                                ft.ElevatedButton(
                                    "Открыть на fantlab.ru",
                                    on_click=lambda _: webbrowser.open_new(book_info['link'])
                                ),
                                ft.ElevatedButton(
                                    "Назад",
                                    on_click=lambda _: page.go("/main")
                                )
                            ]
                        ),
                        expand=True
                    )
                ],
                expand=True
            )
        ]
