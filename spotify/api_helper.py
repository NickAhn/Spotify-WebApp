# Script using spotify_api with more complex functionalities needed for the website
# TODO: This is messy. organize all api calls in one .py file.
from time import time
import spotify.spotify_api as spotify_api
from datetime import date
import pandas as pd
import json

PLAYLIST_ID = "6npTzd1QgVwlJ52QSbEXDJ"

'''
Description: Clear, and update Playlist with User's Top Songs
Params: 
    auth_header
    playlist_id - Found by copying Playlist's link
Return: List containing data of the Songs added
'''
def updateTopSongs(auth_header:dict, playlist_id:str) -> dict:
    print("- Getting ", spotify_api.getCurrentUserProfile()['display_name'], "'s Top Items -")
    topItems = spotify_api.getUserTopItems("short_term")
    uri_list = []
    for i in topItems['items']:
        uri_list.append(i['uri'])
    
    print("- Updating Playlist -")
    spotify_api.updatePlaylist(auth_header, playlist_id, uri_list)

    return get_top_songs_data(topItems)


''' 
Description: Get User Top Track's relevant data 
            (name, artist, album, image, and uri of the top tracks)
Params:
    auth_header - Authentication Header (saved in Flask.Session['auth_header'])
    time_range - short_term (past 4 weeks) / medium_term (past 6 months) / long_term (past year)
Return: List of Dictionaries with data
'''
def get_top_songs_data(auth_header:dict, time_range:str) -> list:
    top_items = spotify_api.getUserTopItems(auth_header=auth_header, time_range=time_range)

    data = []
    for count, i in enumerate(top_items['items'], start=1):
        # image url [2] = 64 x 64
        data.append({
            'name': i['name'],
            'artist': i['artists'][0]['name'],
            'album': i['album']['name'],
            'image': i['album']['images'][2]['url'],
            'uri':i['uri']
        })
    
    json_data = json.dumps(data, indent=4)
    print(json_data)
    with open("nickahn.json", "w") as f:
        f.write(json_data)

    return data
    

# dic:data = json parsed using getTopSongsData()
def printTopSongs(data):
    for count, track in enumerate(data['tracks'], start=1):
        print(count, track['artist'], "-", track['name'])
