# Handle Spotify API Requests
from curses import KEY_A1
from re import A
import requests
import base64
import json
from secret import client_id, secret, refresh_token

# Refresh Spotify Authentication Token previously received in authenticate.py
# - Must have refresh_token in secrets.py


# Class to handle all Spotify API's requests
class api():
    def __init__(self) -> None:
        secrets_data = json.load(open('secrets.json', 'r'))
        self.token = secrets_data['access_token']
        self.refresh_token = secrets_data['refresh_token']
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
    
    def refreshAccessToken(self):
        print("- Refreshing Access Token -")
        TOKEN_URL = 'https://accounts.spotify.com/api/token'

        # Create HEADER by encoding message to 64 bit
        message = f"{client_id}:{secret}"
        encodedData = base64.b64encode(bytes(message, "ISO-8859-1")).decode("ascii")

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        header = {
            'Authorization': f"Basic {encodedData}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        r = requests.post(url=TOKEN_URL, data=data, headers=header)
        token = r.json()['access_token']
        return token


    def getCurrentUserProfile(self):
        endpoint = "https://api.spotify.com/v1/me"

        response = requests.get(url=endpoint, headers=self.header)
        return response.json()


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
        
        request_body = {
            'uris': uri_list
        }

        # response = requests.put(url=endpoint, headers=self.header, params=query)
        response = requests.put(url=endpoint, headers=self.header, data=json.dumps(request_body))

        json_data = response.json()
        return json_data

    def getAvailableGenreSeeds(self):
        endpoint = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

        response = requests.put(url=endpoint, headers=self.header)
        print(response)
        json_data = response.json()
        return json_data



TESTING = False
if TESTING:
    api_test = api(refreshAccessToken())
    topItems = api_test.getUserTopItems("short_term")

    def gettinData():        
        data = {}
        for count, i in enumerate(topItems['items'], start=1):
            data[count] = {
                'name': i['name'],
                'artist': i['artists'][0]['name'],
                'uri':i['uri']
            }

        print(json.dumps(data, indent=2))

    test = api_test.getAvailableGenreSeeds()
    print(type(test))
    

    #TODO: get genre by artist ID
    '''
        gather data to see genres of top 20 songs, then print most prominent genres
    '''
    def gettingTrackGenre():
        for i in topItems['items']:
            print(i['name'], i['type'], sep=" ")

    # gettinData()
