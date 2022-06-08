# Handle JSONbin API requests
# jsonbin.io documentation: https://jsonbin.io/api-reference/bins/get-started
from secrets import jsonbin_masterkey
import requests


# PUT request to update json bin in the jsonbin.io database
# Params: 
# - string:bin_id,
# - dic:json_data
# Return: 
def writeDB(bin_id, json_data):
    print(" - Writing DB - ")
    endpoint = f"https://api.jsonbin.io/v3/b/{bin_id}"

    headers = {
        'Content-Type': "application/json",
        'X-Master-Key': jsonbin_masterkey
    }

    response = requests.put(url=endpoint, headers=headers, json=json_data)
    json_data = response.json()
    print(json_data)
    return json_data



