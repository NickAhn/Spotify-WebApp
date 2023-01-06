# script to Authenticate and get the Access Token and Refresh Token
# for the Spotify API (to used in main.py)

import base64
from textwrap import indent
import requests
# from secret import client_id, secret, redirect_uri
import urllib.parse
import json

with open('secrets.json') as json_file:
    data = json.load(json_file)

# Define scope of permissions (space separated)
SCOPE = 'playlist-modify-public user-top-read'
client_id = data['client_id']
secret = data['secret']
redirect_uri = "http://127.0.0.1:5000/callback/"


def requestUserAuthorization() -> str:
    '''
    Get the Authorization Code to be used in getAccessToken()
    Return: URL string with authorization code
    '''
    print("- Redirecting to AUTH_URL -")
    query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': SCOPE
    }
    AUTH_URL = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)

    return AUTH_URL
    
    
def getAccessHeader(auth_code: str):
    '''
    Get Access Token to be used for OAuth
    Params:
     - auth_code : Authentication code to be used in POST request's payload
    Return: Header to be used for API requests
    '''
    print("\n- Getting Access Token -")
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

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

    r = requests.post(TOKEN_URL, headers=headers, data=payload)
    r_json = r.json()
    print(r_json)
    access_token, refresh_token = r_json['access_token'], r_json['refresh_token']

    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header


# Not currently being used #
# def refreshAccessToken():
#     '''
#     refresh Access Token after it expires
#     '''
#     print("- Refreshing Access Token -")
#     TOKEN_URL = 'https://accounts.spotify.com/api/token'

#     # Create HEADER by encoding message to 64 bit
#     message = f"{client_id}:{secret}"
#     encodedData = base64.b64encode(bytes(message, "ISO-8859-1")).decode("ascii")

#     data = {
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token
#     }

#     header = {
#         'Authorization': f"Basic {encodedData}",
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     r = requests.post(url=TOKEN_URL, data=data, headers=header)
#     token = r.json()['access_token']
#     return token





