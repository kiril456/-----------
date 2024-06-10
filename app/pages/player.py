import flet as ft
from tinytag import TinyTag
from app.function import get_songs_data

class Player(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.state = ""
        self.index = 0
        self.is_playing = False
        self.sequence_tracks = []
        self.count = 1
        self.current_position = 0
        
    def build(self): 
        self.create_tracks()
        
        self.current_time = ft.Text(value="0:00")
        self.remaining_time = ft.Text(value="0:00")
        
        self.name = ft.Text(weight=ft.FontWeight.BOLD, size=15)
        self.author = ft.Text(color="grey", size=12)
        self.image = ft.Image(
            width=60,
            height=60,
            fit=ft.ImageFit.CONTAIN,
            border_radius=10
        )
        
        self.slider = ft.Slider(
            expand=True,
            value=0,
            active_color="green",
            on_change=self.change_position_track,
        )
        
        self.volume_icon = ft.Icon(name=ft.icons.VOLUME_DOWN)
        
        self.volume_slider = ft.Slider(
            width=150,
            min=0,
            max=100,
            divisions=100,
            value=50,
            label="{value}",
            active_color="green",
            on_change=self.volume_change
        )
        
        self.next_track_btn = ft.IconButton(
            icon=ft.icons.SKIP_NEXT,
            icon_size=25,
            icon_color="white",
            on_click=self.next_track,
        )
        
        self.previous_track_btn = ft.IconButton(
            icon=ft.icons.SKIP_PREVIOUS,
            icon_size=25,
            icon_color="white",
            on_click=self.previous_track,
        )
        
        self.minus_15_btn = ft.IconButton(
            icon=ft.icons.ROTATE_LEFT_ROUNDED,
            icon_size=25,
            icon_color="white",
            on_click=self.minus_15_second,
            tooltip="-15"
        ) 
        
        self.plus_15_btn = ft.IconButton(
            icon=ft.icons.ROTATE_RIGHT_ROUNDED,
            icon_size=25,
            icon_color="white",
            on_click=self.plus_15_second,
            tooltip="+15"
        ) 
        
        self.play_btn = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
            icon_size=45, 
            icon_color="white", 
            on_click=self.play_track,
            selected=False,
            style=ft.ButtonStyle(color={"selected": ft.colors.WHITE})
        )
        
        self.view = ft.Container(
            height=100,
            bgcolor="black",
            expand=True,
            padding=ft.padding.only(left=10, right=10),
            content=ft.Row(
                expand=1,
                controls=[
                    ft.Column(
                        expand=1,
                        controls=[
                            ft.Row(
                                [
                                    ft.Column([
                                        
                                    ],
                                    spacing=0)
                                ],
                                scroll=ft.ScrollMode.ADAPTIVE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        expand=2,
                        controls=[
                            ft.Row(
                                [
                                    self.minus_15_btn,
                                    self.previous_track_btn,
                                    self.play_btn,
                                    self.next_track_btn,
                                    self.plus_15_btn
                                ],
                                alignment="center",     
                            ),
                            ft.Row(
                                [
                                    self.current_time,
                                    self.slider,
                                    self.remaining_time
                                ],
                                alignment="center",
                                spacing=0,
                            ),  
                        ],
                        alignment="center",
                        spacing=0,
                    ),
                    ft.Column(
                        expand=1,
                        controls=[
                            ft.Row(
                                [
                                    self.volume_icon,
                                    self.volume_slider
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                vertical_alignment="center",
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10
            ),
        )
        
        return self.view
        
    def play_track(self, e):
        if self.state == "playing":
            self.state = "paused"
            self.play_btn.icon = ft.icons.PLAY_CIRCLE
            self.page.overlay[self.index].pause()
        elif self.state == "paused": 
            self.state = "playing"
            self.play_btn.icon = ft.icons.PAUSE_CIRCLE
            self.page.overlay[self.index].resume()
            
        self.update()
              
    def check_state(self, e):
        if e.data == "completed":
            self.index += 1
            if self.index == len(self.page.overlay):
                self.index = 0
            self.new_track()
            self.play_btn.icon = ft.icons.PAUSE_CIRCLE
            self.update()
        
    def next_track(self, e):
        self.page.overlay[self.index].pause()
        self.index += 1
        if self.index == len(self.page.overlay):
            self.index = 0
        self.add_to_sequence(self.index)
        self.new_track()
        self.update()
    
    def previous_track(self, e):
        if len(self.sequence_tracks) > 1:
            print(int(self.index))
            self.page.overlay[int(self.index)].pause()
            tmp = self.sequence_tracks.copy()
            tmp.reverse()
            self.index = tmp[self.count]
            self.new_track()
            if tmp[-1] == self.index:
                return
        self.count += 1
        self.page.update()    
    
    def add_to_sequence(self, index):
        if index in self.sequence_tracks:
            self.sequence_tracks.remove(index)
            
        self.sequence_tracks.append(index)
        
        tracks = []
        with open('app/pages/recently_track.txt', 'r', encoding='utf-8') as file:
            tracks = file.readlines()
            
        tracks = [line.strip() for line in tracks]
        
        if str(index) in tracks:
            tracks.remove(str(index))
        
        tracks.append(str(index))
        with open('app/pages/recently_track.txt', 'w', encoding='utf-8') as file:
            for line in tracks:
                file.write(line + '\n')

        self.update()
      
    def change_track_time(self, index):
        audio = TinyTag.get(self.page.overlay[index].src)
        self.current_time.value = "0:0"
        self.remaining_time.value = self.converter_time(audio.duration * 1000)
        self.update()
            
    def new_track(self):
        self.change_track_time(self.index)
        self.load_info(self.index)
        self.page.views[0].controls[0].controls[2].insert_data()
        if self.state == "playing":
            self.page.overlay[self.index].play()
            
    def play_card(self, e):
        id = int(e.control.data) - 1
        
        if self.is_playing:
            self.page.overlay[self.index].pause()
            
        self.page.overlay[id].play()
        self.play_btn.icon = ft.icons.PAUSE_CIRCLE
        
        self.add_to_sequence(id)
        self.change_track_time(id)
        self.load_info(id)
        
        self.is_playing = True
        self.state = "playing"
        self.index = id
        self.update()

    def progress_change(self, e):
        audio = TinyTag.get(self.page.overlay[self.index].src)
        self.current_time.value = self.converter_time(e.data)
        self.current_position = e.data
        self.slider.value = (float(e.data) * 1.0) / float(audio.duration * 1000)
        self.update()

    def change_position_track(self, e):
        audio = TinyTag.get(self.page.overlay[self.index].src)
        if audio.duration:
            new_position = int(audio.duration * 1000 * e.control.value)
            self.page.overlay[self.index].seek(new_position)
        else:
            print("Audio duration is not available, cannot seek")
        
        self.update()

    def create_tracks(self):
        self.page.overlay.clear()
        songs = get_songs_data()
        for k in songs:
            audio = ft.Audio(
                src=songs[k]['src'],
                autoplay=False,
                data=k,
                volume=0.5,
                release_mode=ft.audio.ReleaseMode.STOP,
                on_position_changed=self.progress_change,
                on_state_changed=self.check_state,
            )
            self.page.overlay.append(audio)

    def load_info(self, index):
        data = get_songs_data()
        self.image.src = data[str(index + 1)]['image']
        self.name.value = data[str(index + 1)]['name']
        self.author.value = f"{data[str(index + 1)]['author']}, {data[str(index + 1)]['feat']}"
        
        if len(self.view.content.controls[0].controls[0].controls) == 1:
            self.view.content.controls[0].controls[0].controls.insert(0, self.image)
        
        if len(self.view.content.controls[0].controls[0].controls[1].controls) == 0:
            self.view.content.controls[0].controls[0].controls[1].controls.append(self.name)
            self.view.content.controls[0].controls[0].controls[1].controls.append(self.author)

        self.update()

    def volume_change(self, e):
        v = e.control.value
        
        self.page.overlay[self.index].volume = 0.01 * v
        self.page.overlay[self.index].update()
        
        if v == 0:
            self.volume_icon.name = ft.icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = ft.icons.VOLUME_DOWN
        elif 50 < v:
            self.volume_icon.name = ft.icons.VOLUME_UP
            
        self.update()

    def converter_time(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        if seconds < 10:
            return f"{minutes}:0{seconds}"
        return f"{minutes}:{seconds}"

    def plus_15_second(self, e):
        if self.is_playing:
            new_position = int(self.current_position) + 15000
            self.page.overlay[self.index].seek(new_position)
        
    def minus_15_second(self, e):
        if int(self.current_position) >= 15000:
            new_position = int(self.current_position) - 15000
            self.page.overlay[self.index].seek(new_position)
            