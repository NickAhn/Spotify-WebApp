# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks

from re import A
import requests
import base64
import json
from secrets import refresh_token, client_id, secret, refresh_token


# Refresh token previously received in authenticate.py
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


class apiHandler():
    def __init__(self, token) -> None:
        self.token = token
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }

    # GET request to get User's Top Items
    # Param: string:accessToken, str:time_range
    # returns a json object with User's Top Tracks
    # TODO: test with new header
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
    # Params: string:token; string:playlist_id; list:tracks = list of track uri's
    # Return: a snapshot ID for the playlist
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


api = apiHandler(refreshAccessToken())
topItems = api.getUserTopItems("short_term")
playlist_id = "6C95koZYc4e8qG1Fnu2C25"

# songs_uris = ''
# for i in topItems['items']:
#     # print(i['uri'])
#     # print(i['name'])
#     # print(i['id'], end="\n\n")
#     songs_uris += i['uri']
#     #TODO: find a more elegant way to do this
#     if(i != topItems['items'][-1]):
#         songs_uris += ","

# addSongsToPlaylist(token, "6C95koZYc4e8qG1Fnu2C25", songs_uris)

# createPlaylist(token, "31gdfhbyzslosy6wycwpllk5ab6q", "test", True, "Playlist created with Spotify API")
# print(json.dumps(topItems, indent=2))

