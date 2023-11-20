import webbrowser

import flet as ft
from notifypy import Notify

from info_parsers import FantlabParser, FlibustaParser


class MainView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.flibusta_parser = FlibustaParser()

        self.author_books_datatable = ft.Ref[ft.DataTable]()
        self.author_text_field = ft.Ref[ft.TextField]()

        self.page = page

    def render(self):
        return ft.Column(
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    margin=ft.margin.all(8),
                    content=ft.TextField(
                        label="Автор",
                        ref=self.author_text_field,
                        on_submit=self.on_submit_handler,
                        border_color="white",
                        border_radius=0,
                        border_width=2,
                    ),
                ),
                ft.Container(
                    border=ft.border.all(2, "white"),
                    margin=ft.margin.only(left=8, top=0, right=8, bottom=8),
                    content=ft.Column(
                        scroll=ft.ScrollMode.HIDDEN,
                        controls=[
                            ft.DataTable(
                                column_spacing=4,
                                width=float("inf"),
                                ref=self.author_books_datatable,
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

    def on_submit_handler(self, event):
        value = event.control.value
        self.author_text_field.current.value = ""
        self.author_books_datatable.current.rows = []

        self.page.title = "Library Manager"
        self.page.update()

        if author := FantlabParser.get_author_info(value):
            self.page.title = f"Автор: {value}"
            self.page.update()

            for index, book in enumerate(author.books, 1):
                self.author_books_datatable.current.rows.append(
                    ft.DataRow(
                        on_select_changed=self.on_select_changed_handler,
                        cells=[
                            ft.DataCell(ft.Text(f"{index}")),
                            ft.DataCell(ft.Text(book.name)),
                            ft.DataCell(ft.Text(book.type)),
                            ft.DataCell(ft.Text(book.year)),
                            ft.DataCell(ft.Text(book.rating)),
                            ft.DataCell(ft.Text(author.surname)),
                            ft.DataCell(ft.Text(book.link)),
                        ],
                    ),
                )

            self.page.update()
        else:
            notification = Notify()
            notification.title = "Library Manager"
            notification.message = f"'{value}' не найден"
            notification.send()

    def on_select_changed_handler(self, event):
        book_name = event.control.cells[1].content.value
        author_name = event.control.cells[-2].content.value

        self.flibusta_parser.get_books(author_name, book_name)
