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



# get playlist
playlistId = "28aaNsSVEfa0V3R6s5hXHp?si=0666e5bbf57a4eaa"
playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
headers = {
    "Authorization": "Bearer " + token
}

res = requests.get(url=playlistUrl, headers=headers)
if res.status_code != 200:
    print("Error: status code ", res.status_code)
    sys.exit()

response_json = res.json()
# response_json = json.dumps(res.json(), indent=2)

for i in response_json["tracks"]["items"]:
    print(i["track"]["name"])




