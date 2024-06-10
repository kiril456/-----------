import flet as ft
import filetype
from app.function import get_songs_data
import json

class CreatePlaylistPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = 3
        self.info = {
            "name": "",
            "image": "",
            "songs_id": []
        }

    def build(self): 
        self.playlist_name = ft.TextField(label="Add name", border_radius=10, width=300)
        
        self.playlists = ft.Row(wrap=True, run_spacing=10)
        self.add_playlist()
        
        self.pick_image = ft.FilePicker(on_result=self.pick_image_result)
        self.selected_image = ft.Text()
        
        self.add_track_btn = ft.ElevatedButton(text="Add", color="black", bgcolor="#1eb954", width=100, height=40, on_click=self.create_playlist) 
        
        self.upload_image = ft.ElevatedButton(
            "Pick image",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_image.pick_files(
                allow_multiple=True
            ),
            color="blue"
        )
        
        self.view = ft.Container(
            expand=True,
            bgcolor="#212121",
            padding=ft.padding.only(left=60, right=60, top=30),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row([ft.Text(value="Create Playlist", size=23, color="white", weight=ft.FontWeight.BOLD)], alignment="center"),
                    ft.Row(
                        [
                            self.playlist_name,
                            self.pick_image,
                            self.upload_image,
                            self.selected_image,
                            self.add_track_btn,
                        ],
                        spacing=10,
                        alignment="center",
                        wrap=True,
                    ),
                    ft.Column([    
                        ft.Text(value="Playlists", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.playlists
                        ], wrap=True)
                    ], spacing=20)
                ], 
                spacing=30,
                expand=True
            )
        )
         
        return self.view
        
    def pick_image_result(self, e: ft.FilePickerResultEvent):
        file = e.files[0].path
        
        if filetype.is_image(file):
            self.selected_image.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            self.info['image'] = file
            self.upload_image.color = "green"
        else:
            self.upload_image.color = "red"
            self.selected_image.value = f"{e.files[0].name} is not image"
        
        self.update()
        
    def create_playlist(self, e):
        index = 0
        self.info['name'] = self.playlist_name.value
        data = self.get_playlists()
        name = self.info['name']
        image = self.info['image']
        songs = self.info['songs_id']
        
        if data:
            index = str(int(list(data.keys())[-1]) + 1)
            
        if len(name) < 2:
            print("name")
            return
        elif not image:
            image = "app\songs\images\playlist.jpg"
        
        data[index] = self.info
        with open("app\pages\playlists.json", "w") as file:
            json.dump(data, file, indent=4)
        
        playlist = self.playlist_card(index, image, name, songs)
        self.playlists.controls.append(playlist)
        
        self.playlist_name.value = ""
        self.selected_image.value = ""
        
        self.update()

    def add_playlist(self):
        for k, v in self.get_playlists().items():
            self.playlists.controls.append(
                self.playlist_card(k, v['image'], v['name'], v['songs_id'])
            )

    def playlist_card(self, index, image, name, songs):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Stack(
                                [
                                    ft.Image(
                                        src=image,
                                        border_radius=10,
                                        expand=True,
                                    ),
                                ],
                                width=160,
                                height=160,
                            )
                        ],
                        alignment="top",
                        vertical_alignment="top"
                    ),
                    ft.Text(value=name, weight=ft.FontWeight.BOLD, size=15),
                    ft.Text(value=f"Amount of songs: {len(songs)}")
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
            data=index,
            on_click=self.go_playlist
        )
        
    def get_playlists(self):
        with open("app\pages\playlists.json", "r") as file:
            data = json.load(file)
        
        return data
    
    def go_playlist(self, e):
        self.page.session.set("playlist_id", e.control.data)
        self.page.go("/playlist")
