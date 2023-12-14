import flet as ft
from repath import match


class BookView(ft.View):
    def __init__(self, page: ft.Page, route: str):
        super().__init__(route=route)
        self.page = page
        book_uuid = match('/book/:uuid', page.route).groupdict()['uuid']

        book_info = list(filter(lambda b: b['uuid'] == book_uuid, self.page.client_storage.get("books")))[0]

        self.controls = [
            ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        margin=0,
                        width=float("inf"),
                        height=float("inf"),
                        bgcolor=ft.colors.GREEN,
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
                                ft.ElevatedButton("Назад", on_click=lambda _: page.go("/main"))
                            ]
                        ),
                        expand=True
                    )
                ],
                expand=True
            )
        ]
