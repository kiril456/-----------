import flet as ft

class NavBar(ft.NavigationRail):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.selected_index = 0
        self.label_type = ft.NavigationRailLabelType.ALL
        self.min_width = 80
        self.min_extended_width = 200
        self.bgcolor = ft.colors.TRANSPARENT
        self.group_alignment = -0.9
        self.destinations = [
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HOME_OUTLINED, size=30), 
                selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED, size=30), 
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SEARCH_ROUNDED, size=30),
                selected_icon_content=ft.Icon(ft.icons.SEARCH_ROUNDED, size=30),
                padding=ft.padding.only(bottom=60)
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_OUTLINED, size=30),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_MUSIC_ROUNDED, size=30),
            ),
        ]
        self.on_change=self.change_state
        
    def change_state(self, e):
        labels = ["Home", "Search", "Library"]
        if e.control.selected_index == 2:
            self.extended = True if self.extended == False else False
            if self.extended == True:
                for i in range(len(self.destinations)):
                    self.destinations[i].label = labels[i] 
            else:
                for i in range(len(self.destinations)):
                    self.destinations[i].label = None 
            self.page.update()