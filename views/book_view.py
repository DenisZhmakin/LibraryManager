import flet as ft
from repath import match


class BookView(ft.View):
    def __init__(self, page: ft.Page, route: str):
        super().__init__(route=route)
        self.page = page
        book_uuid = match('/book/:uuid', page.route).groupdict()['uuid']

        book_info = list(filter(lambda b: b['uuid'] == book_uuid, self.page.client_storage.get("books")))[0]

        self.controls = [
            ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(book_info['name']),
                    ft.Text(self.page.client_storage.get("author")),
                    ft.ElevatedButton("Назад", on_click=lambda _: page.go("/main")),
                ]
            )
        ]


