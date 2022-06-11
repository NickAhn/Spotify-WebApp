# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks
import spotify_api
import jsonbin_api


PLAYLIST_ID = "6npTzd1QgVwlJ52QSbEXDJ"
SPOTIFY_API = spotify_api.api(spotify_api.refreshAccessToken())
    

def updateTopSongsDB():
    topItems = SPOTIFY_API.getUserTopItems("short_term")

    uris = {}
    for track in topItems['items']:
        uris[track['name']] = track['uri']

    jsonbin_api.writeDB("62a0f04905f31f68b3ba0439", uris)

    return uris


def updateTopSongs(playlist_id):
    print("- Getting ", SPOTIFY_API.getCurrentUserProfile()['display_name'], "'s Top Items -")
    topItems = SPOTIFY_API.getUserTopItems("short_term")
    uri_list = []
    for i in topItems['items']:
        uri_list.append(i['uri'])
    
    print("- Updating Playlist -")
    return SPOTIFY_API.updatePlaylist(playlist_id, uri_list)


updateTopSongs(PLAYLIST_ID)
print("Weekly Bops Updated Successfully!")

