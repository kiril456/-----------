import flet as ft
 
 
class Navbar(ft.UserControl):
    def __init__(self, page):
        super().__init__()   
        self.page = page
        self.index = page.session.get("index")
        self.top_nav_items = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HOME_OUTLINED, size=30), 
                selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED, size=30), 
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SEARCH_ROUNDED, size=30),
                selected_icon_content=ft.Icon(ft.icons.SEARCH_ROUNDED, size=30),
            ),
        ]
        
        self.bottom_nav_items = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_OUTLINED, size=30),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_ROUNDED, size=30),
            ),
        ]
        
        self.create_nav_items = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ADD_CIRCLE_ROUNDED, size=30),
                selected_icon_content=ft.Icon(ft.icons.ADD_CIRCLE_ROUNDED, size=30),
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PLAYLIST_ADD_CIRCLE_ROUNDED, size=30),
                selected_icon_content=ft.Icon(ft.icons.PLAYLIST_ADD_CIRCLE_ROUNDED, size=30),
            ),
        ]
        
        self.top_nav_rail = ft.NavigationRail(
            selected_index=self.index,
            label_type="all",
            destinations=self.top_nav_items,
            bgcolor="#212121",
            min_width=80,
            min_extended_width=200,
            height=240,
            on_change=self.go_pages,
        )
        
        self.bottom_nav_rail = ft.NavigationRail(
            selected_index=None,
            label_type="all",
            destinations=self.bottom_nav_items,
            bgcolor="#212121",
            min_width=80,
            min_extended_width=200,
            on_change=self.extended_nav,
            height=50,
        )
        
        self.create_nav_rail = ft.NavigationRail(
            selected_index=None,
            label_type="all",
            destinations=self.create_nav_items,
            bgcolor="#212121",
            min_width=80,
            min_extended_width=200,
            height=110,
            on_change=self.go_playlist,
        )
 
    def build(self):
        self.view = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row(
                        [
                            self.top_nav_rail,   
                        ],
                    ),
                    border_radius=10,
                    bgcolor="#212121",
                    height=120,
                    margin=0,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            self.bottom_nav_rail,
                            self.create_nav_rail,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    border_radius=10,
                    bgcolor="#212121",
                    expand=True,
                ),
                
            ], spacing=10),
            margin=ft.margin.all(0),
            bgcolor="black",
            border_radius=10,
            expand=True,
        )
        return self.view
        
        
    def extended_nav(self, e):
        top_labels = ["Home", "Search"]
        bottom_labels = ["Library", "Add Track", "Create Playlist"]
        if e.control.selected_index == 0:
            self.top_nav_rail.extended = True if self.top_nav_rail.extended == False else False
            self.bottom_nav_rail.extended = True if self.bottom_nav_rail.extended == False else False
            self.create_nav_rail.extended = True if self.create_nav_rail.extended == False else False
            if self.top_nav_rail.extended == True and self.bottom_nav_rail.extended == True and self.create_nav_rail.extended == True:
                for i in range(len(self.top_nav_items)):
                    self.top_nav_items[i].label = top_labels[i] 
                self.bottom_nav_items[0].label = bottom_labels[0]
                self.create_nav_items[0].label = bottom_labels[1]
                self.create_nav_items[1].label = bottom_labels[2]
            else:
                for i in range(len(self.top_nav_items)):
                    self.top_nav_items[i].label = None 
                self.bottom_nav_items[0].label = None 
                self.create_nav_items[0].label = None 
                self.create_nav_items[1].label = None 
        
        e.control.selected_index = None    
        
        self.update()
            
    def go_pages(self, e):
        self.page.session.set("index", e.control.selected_index)
        self.create_nav_rail.selected_index = None

        match e.control.selected_index:
            case 0:
                self.page.go('/')
            case 1: 
                self.page.go('/search')
        
        self.update()        
        
    def go_playlist(self, e):
        self.top_nav_rail.selected_index = None
        
        match e.control.selected_index:
            case 0:
                self.page.go('/add_track')
            case 1:
                self.page.go('/create_playlist')
                
        self.update()
