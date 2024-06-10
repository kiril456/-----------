import flet as ft
import json
import math
from app.function import get_songs_data

class PlaylistPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = 3
        self.index = self.page.session.get("playlist_id")


    def build(self):
        playlist = self.get_playlist()[self.index]
        
        self.playlist_songs = ft.Column()
        self.get_playlist_songs()
        
        self.songs = ft.Column()
        
        self.view = ft.Container(
            expand=True,
            bgcolor="#212121",
            border_radius=10,
            content=ft.Column(
                [
                    ft.Column([
                        ft.Row([
                            ft.Container(
                                expand=True,
                                bgcolor="red",
                                height=250,
                                border_radius=10,
                                padding=20,
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.Alignment(0.8, 1),
                                    colors=[
                                        "#333333",
                                        "#606060",
                                    ],
                                    tile_mode=ft.GradientTileMode.MIRROR,
                                    rotation=math.pi / 3,
                                ),
                                content=ft.Row([
                                    ft.Container(
                                        width=200,
                                        height=200,
                                        border_radius=10,
                                        content=ft.Image(
                                            src=playlist['image'],
                                            border_radius=10,
                                            expand=True,
                                        ),
                                    ),
                                    
                                    ft.Column([
                                        ft.Text(value="Public Playlist", size=18),
                                        ft.Text(value=playlist['name'], size=40, weight=ft.FontWeight.BOLD),
                                    ], alignment="end")
                                ], spacing=20)
                            )
                        ]),
                        ft.Row([
                            ft.Container(
                                expand=True,
                                border_radius=10,
                                padding=20,
                                content=ft.Column([
                                    self.playlist_songs,
                                    ft.Text(value="Let's find something for your playlist", size=24, weight=ft.FontWeight.BOLD),
                                    ft.TextField(
                                        width=425,
                                        height=50,
                                        border_radius=10,
                                        hint_text="Search for songs",
                                        prefix_icon=ft.icons.SEARCH,
                                        bgcolor="#303030",
                                        border_color="#303030",
                                        on_change=self.find_track
                                    ),
                                    self.songs,
                                ], spacing=20, alignment="start", horizontal_alignment=ft.CrossAxisAlignment.START)
                            ),
                        ])
                    ],
                        expand=True,
                        spacing=10,
                        alignment="start",
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    )
                ], 
                spacing=40,
                expand=True,
                scroll=ft.ScrollMode.ALWAYS
            )
        )
        
        return self.view
    
    def get_playlist(self):
        with open("app\pages\playlists.json", "r") as file:
            data = json.load(file)
        
        return data
    
    def find_track(self, e):
        data = get_songs_data()
        value = e.control.value
        
        if value:
            for i in data:
                if value.lower() in data[i]['name'].lower():
                    self.songs.controls.clear()
                    self.songs.controls.append(self.song_row(data[i]['name'], data[i]['author'], data[i]['image'], i))
                    print(self.songs.controls)
        else:
            self.songs.controls.clear()
                
        self.update()
        
    def song_row(self, name, author, image, index):
        return ft.Container(
            height=70,
            border_radius=10,
            bgcolor="#212121",
            padding=6,
            content=ft.Row([
                ft.IconButton(
                    icon=ft.icons.PLAY_ARROW_ROUNDED,
                    icon_size=28,
                    on_click=self.play_song,
                    data=index
                ),
                ft.Image(
                    src=image,
                    border_radius=10,
                    width=60,
                    height=60
                ),
                ft.Column([
                    ft.Text(value=name, size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(value=author, size=12)
                ]),
                ft.Row([
                    ft.OutlinedButton(
                        text="Add",
                        on_click=self.add_song,
                        style=ft.ButtonStyle(color="green"),
                        data=index,
                    )
                ], alignment=ft.MainAxisAlignment.END, expand=True)
            ]),
            on_hover=self.change_color,
        )
        
    def added_songs(self, name, author, image, index):
        return ft.Container(
            height=70,
            border_radius=10,
            bgcolor="#212121",
            padding=6,
            content=ft.Row([
                ft.IconButton(
                    icon=ft.icons.PLAY_ARROW_ROUNDED,
                    icon_size=28,
                    on_click=self.play_song,
                    data=index
                ),
                ft.Image(
                    src=image,
                    border_radius=10,
                    width=60,
                    height=60
                ),
                ft.Column([
                    ft.Text(value=name, size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(value=author, size=12)
                ]),
                ft.Row([
                    ft.OutlinedButton(
                        text="Delete",
                        on_click=self.delete_song_from_playlist,
                        style=ft.ButtonStyle(color="red"),
                        data=index
                    )
                ], alignment=ft.MainAxisAlignment.END, expand=True)
            ]),
            on_hover=self.change_color,
        )
        
    def change_color(self, e):
        e.control.bgcolor = "#303030" if e.control.bgcolor == "#212121" else "#212121"
        self.update()
        
    def add_song(self, e):
        data = self.get_playlist()
        if e.control.data not in data[self.index]['songs_id']:
            data[self.index]['songs_id'].append(e.control.data)
            
            with open("app\pages\playlists.json", "w") as file:
                json.dump(data, file, indent=4)
                
            self.get_playlist_songs()
        
        self.update()
        
    def get_playlist_songs(self):
        data = self.get_playlist()
        songs = get_songs_data()
            
        self.playlist_songs.controls.clear()
        for id in data[self.index]['songs_id']:
            self.playlist_songs.controls.append(self.added_songs(songs[id]['name'], songs[id]['author'], songs[id]['image'], id))

    def delete_song_from_playlist(self, e):
        data = self.get_playlist()

        data[self.index]['songs_id'].remove(e.control.data)
        
        with open("app\pages\playlists.json", "w") as file:
            json.dump(data, file, indent=4)
            
        self.get_playlist_songs()
        
        self.update()
        
    def play_song(self, e):
        self.page.views[0].controls[1].controls[0].play_card(e)
        self.page.views[0].controls[0].controls[2].insert_data()