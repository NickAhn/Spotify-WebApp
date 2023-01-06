'''
Script to handle all basic requests from the Spotify API.
Reference: https://developer.spotify.com/documentation/web-api/reference/#/
'''
from curses import KEY_A1
from re import A
import requests
import json


def getCurrentUserProfile(auth_header:dict) -> dict:
    '''
    Description: Get detailed profile information about the current user (including the current user's username).
    Params:
        auth_header - Authentication Header (saved in Flask.Session['auth_header'])
    Return: Dictionary with User's Data
    '''
    print("\n- Getting Current User Profile -")
    endpoint = "https://api.spotify.com/v1/me"

    response = requests.get(url=endpoint, headers=auth_header)
    print(response)
    return response.json()


def getUserTopItems(auth_header:dict, time_range:str, type:str = "tracks") -> dict:
    '''
    Description: Get the current user's top artists or tracks based on calculated affinity.
    Params:
        auth_header - Authentication Header (saved in Flask.Session['auth_header'])
        time_range - Over what time frame the affinities are computed. 
                    Valid Values: short_term (past 4 weeks), medium_term (past 6 months, long_term (several years of data)
    Return: Dictionary with Top Items Data
    '''
    endpoint = f"https://api.spotify.com/v1/me/top/{type}"

    queryParameters = {
        'time_range': time_range
    }

    # GET request
    response = requests.get(url=endpoint, headers=auth_header, params=queryParameters)
    return response.json()


# https://developer.spotify.com/documentation/web-api/reference/#/operations/create-playlist
def createPlaylist(auth_header:dict, user_id:str, playlist_name:str, is_public:bool=True, description:str=""):
    '''
    Description: Get the current user's top artists or tracks based on calculated affinity.
    Params:
        auth_header - Authentication Header (saved in Flask.Session['auth_header'])
        time_range - Over what time frame the affinities are computed. 
                    Valid Values: short_term (past 4 weeks), medium_term (past 6 months, long_term (several years of data)
    Return: Dictionary with Top Items Data
    '''
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    
    request_body = {
        "name":playlist_name,
        "public":is_public,
        "description": description
    }

    response = requests.post(url=endpoint, headers=auth_header, data=json.dumps(request_body))
    #TODO: add error handling (try/catch?)

    json_data = response.json()
    return json_data


def addSongToPlaylist(auth_header:dict, playlist_id:str, tracks:str):
    '''
    Decription: Add one or more items to a user's playlist.
    Params: 
     - playlist_id
     - tracks = comma separated list of track uri's (TODO: change to a list type)
    Return: string:snapshot ID for the playlist
    '''
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    query = {
        'uris':tracks
    }

    ## TODO: Fix Error parsing JSON
    # request_body = {
    #     'uris':json.dumps(tracks)
    # }

    response = requests.post(url=endpoint, headers=auth_header, params=query)
    print(response)

    json_data = response.json()
    return json_data



def updatePlaylist(auth_header:dict, playlist_id:str, uri_list:str):
    '''
    Description: Clear playlist and add new songs
    Params: 
    - playlist_id : playlist to be modified
    - uri_list = comma separated list of uri's of the songs to be added
    Return: string with snapshot ID for the playlist
    '''
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    query = {
        'uris': uri_list
    }
    
    request_body = {
        'uris': uri_list
    }

    response = requests.put(url=endpoint, headers=auth_header, data=json.dumps(request_body))

    json_data = response.json()
    return json_data


def getAvailableGenreSeeds(auth_header:dict):
    endpoint = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

    response = requests.put(url=endpoint, headers=auth_header)
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
