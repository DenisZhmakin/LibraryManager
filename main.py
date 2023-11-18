import flet as ft

from views.main_view import MainView


def main(page: ft.Page):
    page.title = "Library Manager"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.window_width = 900
    page.window_max_width = 900
    page.window_min_width = 900

    page.window_height = 600
    page.window_max_height = 600
    page.window_min_height = 600

    page.window_maximizable = False
    page.padding = 0

    main_view = MainView(page=page)

    page.add(
        main_view.render()
    )


if __name__ == "__main__":
    ft.app(target=main)
