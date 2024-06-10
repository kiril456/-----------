import flet as ft
from app.pages.player import Player
from app.pages.navbar import Navbar
from app.pages.search_page import SearchPage
from app.pages.info_elemnt import InfoElement


def views_handler(page):
    return {
        "/search": ft.View(
            route="/search",
            controls=[
                ft.Row(
                    [
                        Navbar(page),
                        SearchPage(page),
                        InfoElement(page)
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
    