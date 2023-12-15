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

        # translations = FantlabParser.get_book_translations(book_info['link'])
        # content = ft.Dropdown(
        #     label="Перевод",
        #     hint_text="Выберите перевод произведения",
        #     options=[
        #         Option(f"{tr['persons']} ({tr['year']} года), {tr['count']} изданий")
        #         for tr in translations
        #     ],
        #     autofocus=True
        # ),

        self.padding = 0

        self.controls = [
            ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        margin=0,
                        width=float("inf"),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(f"Автор: {self.page.client_storage.get('author')}", size=16),
                                ft.Text(f"Название: {book_info['name']}", size=16),
                                ft.Text(f"Тип произведения: {book_info['book_type']}", size=16),
                                ft.Text(f"Год написания: {book_info['year']}", size=16),
                                ft.Text(f"Рейтинг: {book_info['rating']}", size=16),
                            ],
                            expand=True
                        ),
                        expand=60
                    ),
                    ft.Container(
                        margin=0,
                        width=float("inf"),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    "Открыть описание на fantlab.ru",
                                    height=32,
                                    url=book_info['link'],
                                    color=ft.colors.BLACK,
                                    bgcolor=ft.colors.GREEN_700,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.GREEN_700,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "Скачать книгу с флибусты",
                                    height=32,
                                    color=ft.colors.BLACK,
                                    bgcolor=ft.colors.GREEN_700,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "Назад к списку книг",
                                    height=32,
                                    on_click=lambda _: page.go("/main"),
                                    color=ft.colors.BLACK,
                                    bgcolor=ft.colors.GREEN_700,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                )
                            ],
                            expand=True
                        ),
                        expand=40
                    ),
                ],
                expand=True
            ),
        ]
