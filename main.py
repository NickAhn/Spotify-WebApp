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


token = refreshAccessToken()