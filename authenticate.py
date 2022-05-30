# script to Authenticate and get the Access Token and Refresh Token
# for the Spotify API (to used in main.py)

import base64
from textwrap import indent
from urllib import response
import webbrowser
import requests
import json
from secrets import client_id, secret, redirect_uri
import sys
import urllib.parse

# Define scope of permissions (space separated)
SCOPE = 'playlist-modify-public user-top-read'

# Function to get User Authentication Code to be used in getAccessToken()
# params: str:scope = space-separated list of permissions
# return: Authorization Code
def requestUserAuthorization():
    query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': SCOPE
    }
    AUTH_URL = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
    print(AUTH_URL)
    webbrowser.open(AUTH_URL)
    
    temp = input("Enter the url you were redirected to: ")
    auth_code = temp.split("code=")[1]
    return auth_code
    
    
# OAuth to get access token to be used for the Spotify API
# send a POST request to receive the Access Token to be used for the API
# return: tuple with Access Token and Refresh Token
def getAccessToken():
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    # auth_code = requestUserAuthorization('user-top-read playlist-modify-public')
    auth_code = requestUserAuthorization()

    # Create HEADER by encoding message to 64 bit
    message = f"{client_id}:{secret}"
    encodedData = base64.b64encode(bytes(message, "ISO-8859-1")).decode("ascii")


    headers = {
        'Authorization': f"Basic {encodedData}",
        'Content-Type': "application/x-www-form-urlencoded"
    }


    payload = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'redirect_uri': redirect_uri
    }

    # POST request
    r = requests.post(TOKEN_URL, headers=headers, data=payload)
    r_json = r.json()
    print(r_json)
    access_token, refresh_token = r_json['access_token'], r_json['refresh_token']
    print("\nAccess Token: ", access_token)
    print("\nRefresh Token: ", refresh_token)

    return access_token, refresh_token

token = getAccessToken()





