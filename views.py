import flet as ft
from app.pages.player import Player
from app.pages.navbar import Navbar
from app.pages.search_page import SearchPage


def views_handler(page):
    return {
        "/": ft.View(
            route="/",
            controls=[
                ft.Row(
                    [
                        Navbar(page),
                        # # ft.VerticalDivider(width=1),
                        # SearchPage(page),
                        # ft.Column(
                        #     expand=1,
                        #     width = 200,
                        #     controls=[
                        #         ft.Container(bgcolor="#212121", expand=True, border_radius=10),
                        #     ],
                        # )
                    ],
                    expand=True,
                ),
                ft.Row(
                    [
                        Player(page)
                    ],
                )
            ],
            bgcolor="black",   
        ),
        "/search": ft.View(
            route="/search",
            controls=[
                ft.Row(
                    [
                        Navbar(page),
                        SearchPage(page),
                        ft.Column(
                            expand=1,
                            width = 200,
                            controls=[
                                ft.Container(bgcolor="#212121", expand=True, border_radius=10),
                            ],
                        )
                    ],
                    expand=True,
                ),
                ft.Row(
                    [
                        Player(page)
                    ],
                )
            ],
            bgcolor="black",   
        )
    }