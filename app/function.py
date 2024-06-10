import json

def get_songs_data():
    with open("app\songs\songsinfo.json", "r") as json_file:
        data = json.load(json_file)
        
    return data