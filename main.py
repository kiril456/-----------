import flet as ft
from views import views_handler
from app.pages.player import Player

class App(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        page.spacing = 0
        page.padding = 0
        page.window_min_height = 700
        page.window_min_width = 800
        page.bgcolor = "black"
        page.window_width = 800
        page.window_height = 800
        
        self.page = page
        self.player = Player(page)
        
        self.init_helper()
        
        
    def init_helper(self):
        self.page.on_route_change = self.route_change
        self.page.go('/search')
        
        
    def route_change(self, route):
        self.page.views.clear()
        self.page.views.append(views_handler(self.page, self.player)[self.page.route])
        self.page.update()
        
        
if __name__ == "__main__":
    ft.app(target=App)