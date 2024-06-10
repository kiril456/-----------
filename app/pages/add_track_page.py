import flet as ft
import json
import filetype
from app.function import get_songs_data

class AddTrack(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = 3
        self.info = {
            "src": "",
            "name": "",
            "image": "",
            "author": "",
            "feat": "",
        }

    def build(self):
        self.name = ft.TextField(label="Name")
        self.author = ft.TextField(label="Author")
        self.feat = ft.TextField(label="Feat")
        
        self.pick_files = ft.FilePicker(on_result=self.pick_file_result)
        self.pick_image = ft.FilePicker(on_result=self.pick_image_result)
        self.selected_file = ft.Text()
        self.selected_image = ft.Text()
        
        self.add_track_btn = ft.ElevatedButton(text="Add", color="black", bgcolor="#1eb954", width=100, height=40, on_click=self.open_dlg_modal) 
        
        self.upload_track = ft.ElevatedButton(
                        "Pick music",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: self.pick_files.pick_files(
                            allow_multiple=True
                        ),
                        color="blue"
        )
        
        self.upload_image = ft.ElevatedButton(
                        "Pick image",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: self.pick_image.pick_files(
                            allow_multiple=True
                        ),
                        color="blue"
        )
        
        self.dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to add this track?"),
                actions=[
                    ft.TextButton("Yes", on_click=self.add_track),
                    ft.TextButton("No", on_click=self.close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.view = ft.Container(
            expand=True,
            bgcolor="#212121",
            padding=ft.padding.only(left=60, right=60, top=30),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Row([ft.Text(value="Add Song", size=23, color="white", weight=ft.FontWeight.BOLD)], alignment="center"),
                    ft.Column(
                        [
                            self.name,
                            self.author,
                            self.feat,
                            self.pick_files,
                            ft.Row(
                                [
                                    self.upload_track,
                                    self.selected_file,
                                ]
                            ),
                            self.pick_image,
                            ft.Row(
                                [
                                    self.upload_image,
                                    self.selected_image,
                                ]
                            ),
                            ft.Row([
                                self.add_track_btn  
                            ], alignment=ft.MainAxisAlignment.END)
                        ],
                        expand=True,
                        spacing=10
                    )
                ], 
                spacing=20,
                expand=True,
            )
        )
         
        return self.view

    def pick_file_result(self, e: ft.FilePickerResultEvent):
        filename = e.files[0].name
        
        if filename[-4::] == ".mp3":
            self.selected_file.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            self.info['src'] = e.files[0].path
            self.upload_track.color = "green"
        else:
            self.upload_track.color = "red"
            self.selected_file.value = f"{e.files[0].name} is not mp3"
        
        self.update()
        
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
        
    def open_dlg_modal(self, e):
        name = self.name
        author = self.author
        file = self.selected_file
        image = self.selected_image
        
        if name and author and file and image:
            self.page.dialog = self.dlg_modal
            self.dlg_modal.open = True
            self.page.update()
        
    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
        
    def add_track(self, e):
        self.close_dlg(e)
        
        name = self.name.value
        author = self.author.value
        feat = self.feat.value
        
        if name and author:
            self.info['name'] = name
            self.info['author'] = author
            self.info['feat'] = feat
            
        flag = True
        for k in self.info:
            if k == "feat":
                continue
            if not self.info[k]:
                flag = False
                
        if flag:
            data = get_songs_data()
            index = str(int(list(data.keys())[-1]) + 1)
            data[index] = self.info
            
            with open("app\songs\songsinfo.json", "w") as file:
                json.dump(data, file, indent=4)
                
            self.page.views[0].controls[1].controls[0].create_tracks()
            
            self.name.value = ""
            self.author.value = ""
            self.feat.value = ""
            self.selected_file.value = ""
            self.selected_image.value = ""
            
            self.upload_image.color = "blue"
            self.upload_track.color = "blue"

            for k in self.info:
                self.info[k] = ""
            
        self.update()
                