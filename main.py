import flet as ft
from repath import match

from views import MainView, BookView


def main(page: ft.Page):
    page.title = "Library Manager"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.client_storage.clear()

    page.window_width = 900
    page.window_max_width = 900
    page.window_min_width = 900

    page.window_height = 600
    page.window_max_height = 600
    page.window_min_height = 600

    page.window_maximizable = False
    page.padding = 0

    def route_change(route: ft.RouteChangeEvent):
        page.views.clear()

        if route.data == "/main":
            page.views.append(
                MainView(page=page, route="/main")
            )

        if "/book" in route.data:
            page.views.append(
                BookView(page=page, route="/book")
            )
        page.update()

    page.on_route_change = route_change
    page.go("/main")


if __name__ == "__main__":
    ft.app(
        target=main
    )
