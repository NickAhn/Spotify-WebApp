# Main Script: get User's Top Tracks within a time range
# Time ranges:
#  - short_term = calculated from several years of data and including all new data as it becomes available
#  - medium_term = approx. last 6 months
#  - long_term) = approx. last 4 weeks
import spotify_api
from datetime import date
import pandas as pd


PLAYLIST_ID = "6npTzd1QgVwlJ52QSbEXDJ"
# SPOTIFY_API = spotify_api.api(spotify_api.refreshAccessToken())
    

# Return: dictionary of ranking:{track name, artist, uri}
def updateTopSongs(playlist_id):
    print("- Getting ", SPOTIFY_API.getCurrentUserProfile()['display_name'], "'s Top Items -")
    topItems = SPOTIFY_API.getUserTopItems("short_term")
    uri_list = []
    for i in topItems['items']:
        uri_list.append(i['uri'])
    
    print("- Updating Playlist -")
    SPOTIFY_API.updatePlaylist(playlist_id, uri_list)

    return getTopSongsData(topItems)


def getTopSongsData(topItems_json):
    data = {
        "playlist_id": PLAYLIST_ID,
        "date": str(date.today()),
        "tracks":[]
    }
    for count, i in enumerate(topItems_json['items'], start=1):
        data["tracks"].append({
            'name': i['name'],
            'artist': i['artists'][0]['name'],
            'album': i['album']['name'],
            'uri':i['uri']
        })

    return data

# dic:data = json parsed using getTopSongsData()
def printTopSongs(data):
    for count, track in enumerate(data['tracks'], start=1):
        print(count, track['artist'], "-", track['name'])


# data = updateTopSongs(PLAYLIST_ID)
# top_songs_data_st= getTopSongsData(SPOTIFY_API.getUserTopItems("short_term"))
# # printTopSongs(top_songs_data_st)
# df = pd.DataFrame(top_songs_data_st['tracks'])
# df.index = df.index + 1
# print(df)

# # print("Weekly Bops Updated Successfully!")

# with open("nickahn.json", "w") as f:
#     # f.write(json.dumps(df.to_json(), indent=4))
#     f.write(df.to_json(indent=4))

