from os import access
from flask import Flask, render_template, redirect, request, session, url_for
import spotify.spotify_auth as spotify_auth
import spotify.spotify_api as spotify_api
import spotify.api_helper as api_helper
import json

app = Flask(__name__)
app.config['TESTING'] = True
app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',
                  ENV='development')


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
    print("AUTH TOKENNNN _ ", auth_token)
    session['auth_header'] = spotify_auth.getAccessHeader(auth_token)
    return redirect(url_for('main'))
# ----------------------------------------------------


@app.route("/main")
def main():
    user_profile = spotify_api.getCurrentUserProfile(session['auth_header'])
    user_profile_picture = user_profile['images'][0]['url']
    top_items = api_helper.get_top_songs_data(session['auth_header'], 'short_term')
    return render_template("main.html", user=user_profile['display_name'], pfp_url=user_profile_picture, top_songs=top_items)


@app.route("/test")
def test():
    topTracks = spotify_api.getUserTopItems(session['auth_header'], "long_term", type='artists')
    json_data = json.dumps(topTracks, indent=4)
    print(json_data)

    return render_template("test.html", items=json_data)

if __name__ == "__main__":
    app.run(debug=True)