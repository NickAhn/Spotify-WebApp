# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks

# jsonbin.io documentation: https://jsonbin.io/api-reference/bins/get-started

from curses import KEY_A1
from re import A
import requests
import base64
import json
from secrets import refresh_token, client_id, secret, refresh_token, jsonbin_masterkey

# jsonbin database id
BIN_ID = "629d746a05f31f68b3b7788f"

# Refresh Spotify Authentication Token previously received in authenticate.py
def refreshAccessToken():
# OAuth to get access token to be used for the Spotify API
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    # Create HEADER by encoding message to 64 bit
    message = f"{client_id}:{secret}"
    encodedData = base64.b64encode(bytes(message, "ISO-8859-1")).decode("ascii")

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    header = {
        'Authorization': f"Basic {encodedData}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(url=TOKEN_URL, data=data, headers=header)
    token = r.json()['access_token']
    return token


# Class to handle all Spotify API's requests
class apiHandler():
    def __init__(self, token) -> None:
        self.token = token
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }

    # GET request to get User's Most Played Tracks info
    # Param: 
    # - str:time_range: can be short_term (past 4 weeks), medium_term (6 months), long_term (1 year)
    # Return: dic:topItems
    def getUserTopItems(self, time_range):
        endpoint = f"https://api.spotify.com/v1/me/top/tracks"

        queryParameters = {
            'time_range': time_range
        }

        # GET request
        response = requests.get(url=endpoint, headers=self.header, params=queryParameters)
        if response.status_code != 200:
            print("Error: status code ", response.status_code)
            print(response)
            return

        topItems = response.json()
        return topItems


    def createPlaylist(self, user_id, playlist_name, is_public=True, description=""):
        endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        
        request_body = {
            "name":playlist_name,
            "public":is_public,
            "description": description
        }

        response = requests.post(url=endpoint, headers=self.header, data=json.dumps(request_body))
        #TODO: add error handling (try/catch?)

        json_data = response.json()
        return json_data


    # POST request to Add one or more items to a user's playlist
    # Params: 
    # - string:playlist_id
    # - string:tracks = comma separated list of track uri's (TODO: change to a list type)
    # Return: string:snapshot ID for the playlist
    def addSongToPlaylist(self, playlist_id, tracks):
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        query = {
            'uris':tracks
        }

        ## TODO: Fix Error parsing JSON
        # request_body = {
        #     'uris':json.dumps(tracks)
        # }

        response = requests.post(url=endpoint, headers=self.header, params=query)
        print(response)

        json_data = response.json()
        print(type(json_data))
        print(json_data)
        return json_data


    # PUT request to clear playlist and add new songs
    # Params: 
    # - string:playlist_id
    # - string:uri_list = comma separated list of uri's of the songs to be added
    # Return: string:snapshot ID for the playlist
    def updatePlaylist(self, playlist_id, uri_list):
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"


        query = {
            'uris': uri_list
        }
        
        #TODO: Fix error parsing JSON
        # request_body = {
        #     'uris': uri_list
        # }

        response = requests.put(url=endpoint, headers=self.header, params=query)
        print(response)

        json_data = response.json()
        print(type(json_data))
        print(json_data)
        return json_data


# PUT request to update json bin in the jsonbin.io database
# Params: 
# - string:bin_id,
# - dic:json_data
# Return: 
def writeDB(bin_id, json_data):
    print(" - Writing DB - ")
    endpoint = f"https://api.jsonbin.io/v3/b/{bin_id}"

    headers = {
        'Content-Type': "application/json",
        'X-Master-Key': jsonbin_masterkey
    }

    response = requests.put(url=endpoint, headers=headers, json=json_data)
    json_data = response.json()
    print(json_data)
    return json_data



api = apiHandler(refreshAccessToken())
topItems = api.getUserTopItems("short_term")
playlist_id = "6C95koZYc4e8qG1Fnu2C25"

test = writeDB("62a0f04905f31f68b3ba0439", topItems)
print(test)

# songs_uris = ''
# for i in topItems['items']:
#     # print(i['uri'])
#     # print(i['name'])
#     # print(i['id'], end="\n\n")
#     songs_uris += i['uri']
#     #TODO: find a more elegant way to do this
#     if(i != topItems['items'][-1]):
#         songs_uris += ","

# api.updatePlaylist(playlist_id, topItems['items'][0]['uri'])

# addSongsToPlaylist(token, "6C95koZYc4e8qG1Fnu2C25", songs_uris)

# createPlaylist(token, "31gdfhbyzslosy6wycwpllk5ab6q", "test", True, "Playlist created with Spotify API")
# print(json.dumps(topItems, indent=2))

