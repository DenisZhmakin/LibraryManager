import flet as ft
from notifypy import Notify

from info_parsers import FantlabParser


class MainView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.parser = FantlabParser()

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
                                width=float("inf"),
                                ref=self.author_books_datatable,
                                border=ft.border.only(bottom=ft.BorderSide(2, 'white')),
                                columns=[
                                    ft.DataColumn(ft.Text("Номер")),
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Год написания"), numeric=True),
                                    ft.DataColumn(ft.Text("Рейтинг"), numeric=True)
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

        self.page.update()

        authors = self.parser.get_authors(value)

        if authors:
            author_info = self.parser.get_author_info(authors[0])

            for index, book in enumerate(author_info.novels, 1):
                self.author_books_datatable.current.rows.append(
                    ft.DataRow(
                        on_select_changed=self.on_select_changed_handler,
                        cells=[
                            ft.DataCell(ft.Text(f"{index}")),
                            ft.DataCell(ft.Text(book.name)),
                            ft.DataCell(ft.Text(f"{book.year}")),
                            ft.DataCell(ft.Text(str(book.rating))),
                            ft.DataCell(ft.Text(str(book.link))),
                        ],
                    ),
                )

                self.page.update()
        else:
            notification = Notify()
            notification.title = "Library Manager"
            notification.message = "Автор не найден"
            notification.send()

    @classmethod
    def on_select_changed_handler(cls, event):
        book_url = event.control.cells[-1].content.value
        print(book_url)
