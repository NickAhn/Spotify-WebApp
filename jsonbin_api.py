# Handle JSONbin API requests
# jsonbin.io documentation: https://jsonbin.io/api-reference/bins/get-started
from secrets import jsonbin_masterkey
import requests

HEADERS = {
        'Content-Type': "application/json",
        'X-Master-Key': jsonbin_masterkey
    }

# PUT request to update json bin in the jsonbin.io database
# Params: 
# - string:bin_id,
# - dic:json_data
# Return: 
def writeDB(bin_id, json_data):
    print(" - Writing DB - ")
    endpoint = f"https://api.jsonbin.io/v3/b/{bin_id}"

    response = requests.put(url=endpoint, headers=HEADERS, json=json_data)
    json_data = response.json()
    print(json_data)
    return json_data


def createDB(bin_name, data):
    print("- Creating JSON Bin", bin_name, " - ")
    endpoint = "https://api.jsonbin.io/v3/b"
    HEADERS["X-Bin-Name"] = bin_name

    response = requests.post(url=endpoint, headers=HEADERS, json=data)
    json_data = response.json()
    return json_data





