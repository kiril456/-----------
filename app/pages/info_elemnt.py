import flet as ft
from app.function import get_songs_data

class InfoElement(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = 1
        
    def build(self):
        self.image = ft.Image(
            border_radius=10,
            width=300,
            height=300
        )
        self.name = ft.Text(size=20, weight=ft.FontWeight.BOLD)
        self.author = ft.Text(size=20)
        self.feat = ft.Text(size=20)
        
        self.view = ft.Container(
            expand=1,
            border_radius=10,
            bgcolor="#212121",
            padding=20,
            content=ft.Row([
                ft.Column([], horizontal_alignment="center", spacing=10)
            ], alignment="center", expand=1)
        )
        
        return self.view
    
    def insert_data(self):
        index = self.page.views[0].controls[1].controls[0].index

        data = get_songs_data()[str(index + 1)]

        self.image.src = data['image']
        self.name.value = data['name']
        self.author.value = f"Author: {data['author']}"
        
        if data['feat']:
            self.feat.value = f"Feat: {data['feat']}"
        else:
            self.feat.value = ""
        
        self.view.content.controls[0].controls.append(self.name)
        self.view.content.controls[0].controls.append(self.image)
        self.view.content.controls[0].controls.append(self.author)
        self.view.content.controls[0].controls.append(self.feat)
        
        self.update()
        