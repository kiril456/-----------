import flet as ft
from views import views_handler
from app.pages.home_page import HomePage
from app.pages.search_page import SearchPage
from app.pages.add_track_page import AddTrack
from app.pages.create_playlist_page import CreatePlaylistPage
from app.pages.playlist_page import PlaylistPage

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
        
        self.init_helper()
        
        
    def init_helper(self):
        self.page.on_route_change = self.route_change
        self.page.go('/search')
        
        
    def route_change(self, route):
        home_page = HomePage(self.page)
        search_page = SearchPage(self.page)
        add_page = AddTrack(self.page)
        create_playlist_page = CreatePlaylistPage(self.page)
        playlist = PlaylistPage(self.page)

        if not self.page.views[0].controls:
            self.page.views.clear()
            self.page.views.append(views_handler(self.page)["/search"])
            
        match self.page.route:
            case "/search":
                self.page.views[0].controls[0].controls[1] = search_page
            case "/":
                self.page.views[0].controls[0].controls[1] = home_page
            case "/add_track":
                self.page.views[0].controls[0].controls[1] = add_page
            case "/create_playlist":
                self.page.views[0].controls[0].controls[1] = create_playlist_page
            case "/playlist":
                self.page.views[0].controls[0].controls[1] = playlist
                
        self.page.update()
        
if __name__ == "__main__":
    ft.app(target=App)