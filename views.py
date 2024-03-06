import flet as ft
from app.elements import Main
from app.player import Player
from app.navbar import NavBar


def views_handler(page):
    return {
        "/": ft.View(
            route="/",
            controls=[
                ft.Row(
                    [
                        NavBar(page),
                        ft.VerticalDivider(width=1),
                        
                    ],
                    expand=True,
                )
            ],
            bgcolor="black",   
            navigation_bar=Player()
        )
    }