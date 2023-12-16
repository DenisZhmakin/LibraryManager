import flet as ft

from parsers import FlibustaParser


class BookView(ft.View):

    def __init__(self, page: ft.Page, route: str, book_info: dict):
        super().__init__(route=route)
        self.page = page
        self.book_info = book_info

        self.padding = 0

        self.controls = [
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(f"Автор: {self.page.client_storage.get('author')}", size=16),
                            ft.Text(f"Название: {book_info['name']}", size=16),
                            ft.Text(f"Тип произведения: {book_info['book_type']}", size=16),
                            ft.Text(f"Год написания: {book_info['year']}", size=16),
                            ft.Text(f"Рейтинг: {book_info['rating']}", size=16),
                        ],
                        expand=55
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Checkbox(
                                        label="Автоматический выбор перевода",
                                        active_color=ft.colors.GREEN_700,
                                        value=True
                                    )
                                ]
                            ),
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
                                on_click=self.download_book_handler,
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
                        expand=45
                    ),
                ],
                expand=True
            ),
        ]

    def download_book_handler(self, _):
        # translations = FantlabParser.get_book_translations(book_info['link'])
        author_fio = FlibustaParser.find_writer_by_query(self.page.client_storage.get('author'))
        books = FlibustaParser.get_book_list(author_fio['fio'].split()[-1], self.book_info['name'])
        print(books)
