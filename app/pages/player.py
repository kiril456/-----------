import flet as ft
from tinytag import TinyTag
import json


class Player(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.state = ""
        self.current_song = int(self.get_id()) - 1
        
        
    def build(self): 
        self.create_tracks()
        self.slider = ft.Slider(
            width=500,
            value=0,
        )
        
        self.play_btn = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
            # selected_icon=ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED, 
            icon_size=45, 
            icon_color="white", 
            on_click=self.toggle_icon_button,
            selected=False,
            style=ft.ButtonStyle(color={"selected": ft.colors.WHITE})
        )
        
        self.view = ft.Container(
            height=100,
            bgcolor="black",
            expand=True,
            content=ft.Row(
                [
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Row(
                                [
                                    self.play_btn,
                                ],
                                alignment="center",
                                
                            ),
                            ft.Row(
                                [
                                    self.slider
                                ],
                                alignment="center",
                            ),  
                        ],
                        alignment="center",
                        spacing=0,
                    ),
                ],
                alignment="center",
                vertical_alignment="center",
            )
        )
        
        return self.view
        
    def toggle_icon_button(self, e, index):
        id = index
        
        if self.state == "" or self.state == "completed":
            self.play_btn.icon = ft.icons.PAUSE_CIRCLE
            if self.state == "completed":
                self.play_btn.icon = ft.icons.PLAY_CIRCLE
            self.page.overlay[id].play()
        elif self.state == "playing":
            self.play_btn.icon = ft.icons.PLAY_CIRCLE
            self.page.overlay[id].pause()
        elif self.state == "paused":
            self.play_btn.icon = ft.icons.PAUSE_CIRCLE
            self.page.overlay[id].resume() 
        elif self.state == "stopped":
            self.page.overlay[id].resume() 
            
            
        self.update()
        
        
    def play_track(self, e):
        id = int(e.control.data) - 1
        
        print(f"Len overlay{len(self.page.overlay)}")

        self.page.overlay[self.current_song].release() 
        # self.page.overlay[id].play() 
        self.toggle_icon_button(e, id)
        
        self.current_song = id
            
            
    def check_changes(self, e):
        self.state = e.data
        print(e.data)
    
    def change_slider(self, e):
        audio = TinyTag.get(self.page.overlay[0].src)
        self.slider.value = (float(e.data) * 1.0) / float(audio.duration * 1000)

        self.update()


    def create_tracks(self):
        self.page.overlay.clear()
        songs = self.get_songs_data()
        for k in songs:
            audio = ft.Audio(
                src=songs[k]['src'],
                autoplay=False,
                data=k,
                on_state_changed=self.check_changes
            )
            self.page.overlay.append(audio)


    def get_songs_data(self):
        with open("app\songs\songsinfo.json", "r") as json_file:
            data = json.load(json_file)
            return data
        
    def get_src_song(self):
        with open("app\songs\songsinfo.json", "r") as json_file:
            data = json.load(json_file)
            for k in data.keys():
                if data[k]['play'] == True:
                    return data[k]['src']
            
        return None
    
    def get_id(self):
        with open("app\songs\songsinfo.json", "r") as json_file:
            data = json.load(json_file)
            for k in data.keys():
                if data[k]['play'] == True:
                    return k
            
        return None