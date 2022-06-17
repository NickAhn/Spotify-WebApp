from os import access
import pandas as pd
from flask import Flask, render_template, redirect, request, session, url_for
import spotify_auth
import json
import spotify_api
import api_helper

app = Flask(__name__)
app.config['TESTING'] = True
app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',
                  ENV='development')

# data = main.getTopSongsData(SPOTIFY_API.getUserTopItems("short_term"))
# df = pd.DataFrame.from_dict(data['tracks'])
# df.index = df.index+1

# headings = df.columns.values
# data = df.values

@app.route("/")
def index():
    return render_template("index.html")

# -------------------- auth -------------------------
@app.route("/auth")
def auth():
    AUTH_URL = spotify_auth.requestUserAuthorization()
    print(AUTH_URL)
    return redirect(AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    session['auth_header'] = spotify_auth.getAccessHeader(auth_token)
    return redirect(url_for('main'))
# ----------------------------------------------------

@app.route("/main")
def main():
    user_profile = spotify_api.getCurrentUserProfile(session['auth_header'])
    user_profile_picture = user_profile['images'][0]['url']
    top_items = api_helper.get_top_songs_data(session['auth_header'], 'short_term')
    return render_template("main.html", user=user_profile['display_name'], pfp_url=user_profile_picture)

if __name__ == "__main__":
    app.run(debug=True)