# Spotify Weekly Top Songs (WIP)
- Python Script to create a playlist with your *short-term* top songs using the Spotify API
- Playlist created will be updated weekly

## Description of files
### main.py
main script of the project. Contains the code to read User's top songs

### authenticate.py
script to make GET requests for user authorization and POST requests to receive Access Token and Refresh Token\
obs: The *refresh()* function in main.py refreshes the Access Token after it expires
HOW TO USE:
1. create a file called *secrets.py*. This is where your *client id*, *client secret*, *authentication token*, and *refresh token* will be stored.


## Future of the Project
I plan to expand this project by adding features such as:
- Creating playlists for different categories
- Blend different playlists
- Group playlists
