import flet as ft
from app.player import Player
from app.navbar import NavBar


class Main(ft.UserControl):
    def __init__(self, page, content=None):
        super().__init__()
        self.page = page
        self.content = content
        
    def build(self):
        return NavBar(self.page)