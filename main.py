import flet as ft

from views.main_view import MainView


def main(page: ft.Page):
    page.title = "Library Manager"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.window_resizable = False
    page.window_height = 500
    page.window_width = 300

    page.padding = 0

    main_view = MainView()

    page.add(
        main_view.render()
    )


if __name__ == "__main__":
    ft.app(target=main)
