import flet as ft


class Player(ft.NavigationBar):
    def __init__(self):
        super().__init__()
        self.bgcolor = "#000000"
        self.height = 100
        self.destinations = []