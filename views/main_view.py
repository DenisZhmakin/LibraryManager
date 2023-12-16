import flet as ft
from notifypy import Notify

from parsers import FantlabParser


class MainView(ft.View):
    def __init__(self, page: ft.Page, route: str):
        super().__init__(route=route)
        self.page = page

        self.author_textfield = ft.Ref[ft.TextField]()
        self.book_datatable = ft.Ref[ft.DataTable]()

        books = self.page.client_storage.get("books")
        author = self.page.client_storage.get("author")

        self.controls = [
            ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        margin=ft.margin.only(left=0, top=0, right=0, bottom=4),
                        content=ft.TextField(
                            label="Автор",
                            ref=self.author_textfield,
                            on_submit=self.on_submit_handler,
                            border_color="white",
                            border_radius=0,
                            border_width=2,
                        ),
                    ),
                    ft.Container(
                        border=ft.border.all(2, "white"),
                        margin=ft.margin.only(left=0, top=4, right=0, bottom=0),
                        content=ft.Column(
                            scroll=ft.ScrollMode.HIDDEN,
                            controls=[
                                ft.DataTable(
                                    column_spacing=70,
                                    width=float("inf"),
                                    ref=self.book_datatable,
                                    columns=[
                                        ft.DataColumn(ft.Text("Номер")),
                                        ft.DataColumn(ft.Text("Название")),
                                        ft.DataColumn(ft.Text("Тип произведения")),
                                        ft.DataColumn(ft.Text("Год написания"), numeric=True),
                                        ft.DataColumn(ft.Text("Рейтинг"), numeric=True),
                                    ],
                                )
                            ],
                        ),
                        expand=True,
                    )
                ],
                expand=True
            )
        ]

        if books and author:
            self.fill_datatable(books, author)

    def on_submit_handler(self, event):
        value = event.control.value
        self.author_textfield.current.value = ""
        self.book_datatable.current.rows = []
        self.page.client_storage.clear()

        self.page.title = "Library Manager"
        self.page.update()

        books = FantlabParser.search_books(value)

        if len(books) > 0:
            self.page.client_storage.set("books", books)
            self.page.client_storage.set("author", value)
            self.fill_datatable(books, value)
        else:
            notification = Notify()
            notification.title = "Library Manager"
            notification.message = f"Автор '{value}' не найден"
            notification.send()

    def fill_datatable(self, books, author):
        self.page.title = f"Автор: {author}"
        self.page.update()

        for index, book in enumerate(books, 1):
            self.book_datatable.current.rows.append(
                ft.DataRow(
                    on_select_changed=self.on_select_changed_handler,
                    cells=[
                        ft.DataCell(ft.Text(f"{index}")),
                        ft.DataCell(ft.Text(book['name'])),
                        ft.DataCell(ft.Text(book['book_type'])),
                        ft.DataCell(ft.Text(book['year'])),
                        ft.DataCell(ft.Text(book['rating'])),
                        ft.DataCell(ft.Text(book['link'])),
                        ft.DataCell(ft.Text(book['uuid'])),
                    ],
                ),
            )

        self.page.update()

    def on_select_changed_handler(self, event):
        book_uuid = event.control.cells[-1].content.value
        self.page.go(f"/book/{book_uuid}")
