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


# Function to get User Authentication Code to be used in getAccessToken()
# params: str:scope = space-separated list of permissions
# return: Authorization Code
def requestUser3(scope):
    query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
    }
    AUTH_URL = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
    print(AUTH_URL)
    webbrowser.open(AUTH_URL)
    
    temp = input("Enter the url you were redirected to: ")
    auth_code = temp.split("code=")[1]
    return auth_code
    
    
def requestUserAuthorization(scope):
    AUTH_URL = 'https://accounts.spotify.com/authorize'

    query = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:5500/index.html',
        'scope': scope
    }

    #make request to the /authorize endpoint
    # change the scope depending on what you want to do
    r = requests.get(AUTH_URL, query)
    print(r.text)
    json_data = r.json()

    print(json_data)
    print(type(json_data))

    auth_code = json_data['code']
    print(" - Auth_code: ", auth_code)
    return auth_code


# OAuth to get access token to be used for the Spotify API
# send a POST request to receive the Access Token to be used for the API
# return: tuple with Access Token and Refresh Token
def getAccessToken(scope):
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    # auth_code = requestUserAuthorization('user-top-read playlist-modify-public')
    auth_code = requestUser3(scope)

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

scope = 'playlist-modify-public user-top-read'
token = getAccessToken(scope)





