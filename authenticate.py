# script to Authenticate and get the Access Token and Refresh Token
# for the Spotify API (to used in main.py)

import base64
import json
from textwrap import indent
from urllib import response
import requests
import json
from secrets import client_id, secret
import sys

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Create a GET request for the User Authorization
def requestUserAuthorization():
    AUTH_URL = 'https://accounts.spotify.com/authorize'

    #make request to the /authorize endpoint
    # change the scope depending on what you want to do
    auth_code = requests.get(AUTH_URL, {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:5500/index.html',
        'scope': 'user-top-read'
    })

    print("Auth_code: ", auth_code)
    return auth_code


# OAuth to get access token to be used for the Spotify API
# send a POST request to receive the Access Token to be used for the API
def getAccessToken(authCode):
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    # Create HEADER by encoding message to 64 bit
    message = f"{client_id}:{secret}"
    messageBytes = message.encode('ascii') #convert to bytes
    base64Bytes = base64.b64encode(messageBytes) #encode it into base64
    base64Message = base64Bytes.decode('ascii') #convert back to string

    headers = {
        'Authorization': f"Basic {base64Message}",
        'Content-Type': "application/x-www-form-urlencoded"
    }


    payload = {
        'grant_type': "authorization_code",
        'code': authCode,
        'redirect_uri': 'http://127.0.0.1:5500/index.html'
    }

    # POST request
    r = requests.post(url, headers=headers, data=payload)
    r_json = r.json()
    print(r_json)
    access_token, refresh_token = r_json['access_token'], r_json['refresh_token']
    print(token)

    return token


auth_code = requestUserAuthorization()
token = getAccessToken(auth_code)
print(token)
# print(json.dumps(topItems), indent=2)





