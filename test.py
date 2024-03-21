import flet as ft
from app.pages.search_page import SearchPage

def main(page: ft.Page):
    
    tmp = SearchPage(page)
    
    print(tmp.song_id)
    
    page.update()
    
ft.app(target=main)