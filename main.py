# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks

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


# GET request to get User's Top Items
# Param: string:accessToken, str:time_range
# returns a json object with User's Top Tracks
def getUserTopItems(accessToken, time_range):
    endpoint = f"https://api.spotify.com/v1/me/top/tracks"

    header = {
        "Authorization": "Bearer " + accessToken
    }

    queryParameters = {
        'time_range': time_range
    }

    # GET request
    response = requests.get(url=endpoint, headers=header, params=queryParameters)
    if response.status_code != 200:
        print("Error: status code ", response.status_code)
        return

    topItems = response.json()
    return topItems

def createPlaylist(token, user_id, playlist_name, is_public, description):
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    request_body = {
        "name":playlist_name,
        "public":is_public,
        "description": description
    }

    response = requests.post(url=endpoint, headers=header, data=json.dumps(request_body))
    if response.status_code != 200:
        print("Error: status code ", response.status_code)
        return

    json_data = response.json()
    return json_data


token = refreshAccessToken()
topItems = getUserTopItems(token, "long_term")
print(type(topItems))
print()
for i in topItems['items']:
    print(i['name'])
    print(i['id'], end="\n\n")

createPlaylist(token, "31gdfhbyzslosy6wycwpllk5ab6q", "test", True, "Playlist created with Spotify API")
# print(json.dumps(topItems, indent=2))

