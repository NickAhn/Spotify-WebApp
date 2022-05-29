import base64
import json
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
    auth_code = requests.get(AUTH_URL, {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:5500/index.html'
        'scope': 'user-top-read'
    })
    print(auth_code)


# OAuth to get access token to be used for the Spotify API
def getAccessToken(clientID, secret):
    # Encode base 64
    message = f"{client_id}:{secret}"
    messageBytes = message.encode('ascii') #convert to bytes
    base64Bytes = base64.b64encode(messageBytes) #encode it into base64
    base64Message = base64Bytes.decode('ascii') #convert back to string

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    # POST request
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']

    return token


def getUserTopItems(acessToken):
    endpoint = "https://api.spotify.com/v1/me/top/type"


    header = {
        "Authorization": "Bearer " + token
    }

    # GET request
    response = requests.get(url=endpoint, headers=header)
    if response.status_code != 200:
        print("Error: status code ", response.status_code)
        return

    topItems = response.json()
    return topItems


token = getAccessToken(client_id, secret)
topItems = getUserTopItems(token)
print(json.dumps(topItems), indent=2)





