import flet as ft

from info_parsers import FantlabParser


class MainView:
    def __init__(self):
        self.parser = FantlabParser()

        self.author_text_field = ft.Ref[ft.TextField]()

    def render(self):
        return ft.Column(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.TextField(
                        label="Автор",
                        ref=self.author_text_field,
                        on_submit=self.on_submit_handler
                    ),
                    margin=ft.margin.all(8)
                )
            ],
            expand=True
        )

    def on_submit_handler(self, event):
        value = event.control.value
        self.author_text_field.current.value = ""
        self.author_text_field.current.page.update()

        author_url = self.parser.get_authors(value)

        print(self.parser.get_author_info(author_url[0]))


