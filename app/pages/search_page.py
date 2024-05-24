import flet as ft
import json

class SearchPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = 3
        self.songs_data = self.get_songs_data()
        self.song_id = ""
        self.state = ""
        
    def build(self):
        self.row_cards = ft.Row(scroll="always", wrap=False, spacing=20)
        self.songs_card()
        
        self.view = ft.Container(
            expand=True,
            bgcolor="#212121",
            padding=20,
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row([
                        ft.TextField(
                            width=350,
                            border_radius=30,
                            hint_text="What do you want to play?",
                            prefix_icon=ft.icons.SEARCH,
                            color="white",
                            selection_color="white",
                            focused_border_color="white",
                            bgcolor="#303030",
                            border_color="#303030",
                        )
                    ]),
                    ft.Column(
                        [
                            ft.Text(value="Songs", size=23, color="white", weight=ft.FontWeight.BOLD),
                            self.row_cards,
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True,
                    )
                ], 
                spacing=20,
                expand=True,
            )
        )
        
        return self.view
    
    
    def songs_card(self):
        for k, v in self.songs_data.items():
            self.row_cards.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Stack(
                                        [
                                            ft.Image(
                                                src=v['image'],
                                                border_radius=10,
                                                expand=True,
                                            ),
                                            ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILLED, 
                                                        icon_color="#1eb954", 
                                                        icon_size=30, 
                                                        right=5, 
                                                        bottom=5,
                                                        bgcolor="black",
                                                        data=k,   
                                                        on_click=self.play_song
                                            ),
                                        ],
                                        width=160,
                                        height=160,
                                    )
                                ],
                                alignment="top",
                                vertical_alignment="top"
                            ),
                            ft.Text(value=v['name'], weight=ft.FontWeight.BOLD, size=15),
                            
                            ft.Text(value=f"{v['author']}, {v['feat']}", size=12)
                        ],
                        alignment="top",
                        horizontal_alignment="center",
                        expand=True
                        
                    ),
                    width=200,
                    height=300,
                    bgcolor="#303030",
                    padding=20,
                    border_radius=10,
                    data=k,
                    # on_click=self.play_song
                )
            )  
    
    def get_songs_data(self):
        with open("app\songs\songsinfo.json", "r") as json_file:
            data = json.load(json_file)
            
            return data
        
    def play_song(self, e):
        self.page.views[0].controls[1].controls[0].play_card(e)
