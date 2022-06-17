# Script using spotify_api with functionalities needed for the website
from time import time
import spotify_api
from datetime import date
import pandas as pd
import json


PLAYLIST_ID = "6npTzd1QgVwlJ52QSbEXDJ"
# SPOTIFY_API = spotify_api.api(spotify_api.refreshAccessToken())
    

# Return: dictionary of ranking:{track name, artist, uri}
def updateTopSongs(auth_header, playlist_id):
    print("- Getting ", spotify_api.getCurrentUserProfile()['display_name'], "'s Top Items -")
    topItems = spotify_api.getUserTopItems("short_term")
    uri_list = []
    for i in topItems['items']:
        uri_list.append(i['uri'])
    
    print("- Updating Playlist -")
    spotify_api.updatePlaylist(auth_header, playlist_id, uri_list)

    return get_top_songs_data(topItems)


# def getTopSongsData(topItems_json):
#     data = {
#         "playlist_id": PLAYLIST_ID,
#         "date": str(date.today()),
#         "tracks":[]
#     }
#     for count, i in enumerate(topItems_json['items'], start=1):
#         data["tracks"].append({
#             'name': i['name'],
#             'artist': i['artists'][0]['name'],
#             'album': i['album']['name'],
#             'uri':i['uri']
#         })

#     return data


def get_top_songs_data(auth_header:dict, time_range:str) -> dict:
    top_items = spotify_api.getUserTopItems(auth_header=auth_header, time_range=time_range)

    data = {}
    for count, i in enumerate(top_items['items'], start=1):
        # image url [2] = 64 x 64
        data[count] = {
            'name': i['name'],
            'artist': i['artists'][0]['name'],
            'album': i['album']['name'],
            'image': i['album']['images'][2]['url'],
            'uri':i['uri']
        }
    
    json_data = json.dumps(data, indent=4)
    # print(json_data)
    with open("nickahn.json", "w") as f:
        f.write(json_data)

    return data
    

# dic:data = json parsed using getTopSongsData()
def printTopSongs(data):
    for count, track in enumerate(data['tracks'], start=1):
        print(count, track['artist'], "-", track['name'])
