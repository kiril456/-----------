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
        
        self.bottom_nav_item = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_OUTLINED, size=30),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_ROUNDED, size=30),
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
            destinations=self.bottom_nav_item,
            bgcolor="#212121",
            min_width=80,
            min_extended_width=200,
            on_change=self.extended_nav,
            height=240,
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
                    content=ft.Row(
                        [
                            self.bottom_nav_rail,   
                        ],
                        vertical_alignment="start"
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
        labels = ["Home", "Search", "Library"]
        if e.control.selected_index == 0:
            self.top_nav_rail.extended = True if self.top_nav_rail.extended == False else False
            self.bottom_nav_rail.extended = True if self.bottom_nav_rail.extended == False else False
            if self.top_nav_rail.extended == True and self.bottom_nav_rail.extended == True:
                for i in range(len(self.top_nav_items)):
                    self.top_nav_items[i].label = labels[i] 
                self.bottom_nav_item[0].label = labels[-1]
            else:
                for i in range(len(self.top_nav_items)):
                    self.top_nav_items[i].label = None 
                self.bottom_nav_item[0].label = None
        
        if e.control.selected_index != None and self.top_nav_rail.selected_index == None:
            self.top_nav_rail.selected_index = None
        else: 
            e.control.selected_index = None
            
        self.update()
        
        
    def go_pages(self, e):
        self.page.session.set("index", e.control.selected_index)
        
        match e.control.selected_index:
            case 0:
                self.page.go('/')
            case 1: 
                self.page.go('/search')
