# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks
import spotify_api
import jsonbin_api


PLAYLIST_ID = "6C95koZYc4e8qG1Fnu2C25"
SPOTIFY_API = spotify_api.apiHandler(spotify_api.refreshAccessToken())
    

def updateTopSongsDB():
    topItems = SPOTIFY_API.getUserTopItems("short_term")

    uris = {}
    for track in topItems['items']:
        uris[track['name']] = track['uri']

    jsonbin_api.writeDB("62a0f04905f31f68b3ba0439", uris)

    return uris

# def updateTopSongsPlaylist():
    # SPOTIFY_API.updatePlaylist()

updateTopSongsDB()



# songs_uris = ''
# for i in topItems['items']:
#     print(i['uri'])
#     # print(i['name'])
#     # print(i['id'], end="\n\n")
#     songs_uris += i['uri']
#     #TODO: find a more elegant way to do this
#     if(i != topItems['items'][-1]):
#         songs_uris += ","

# api.updatePlaylist(playlist_id, topItems['items'][0]['uri'])

# addSongsToPlaylist(token, "6C95koZYc4e8qG1Fnu2C25", songs_uris)

# createPlaylist(token, "31gdfhbyzslosy6wycwpllk5ab6q", "test", True, "Playlist created with Spotify API")
# print(json.dumps(topItems, indent=2))

