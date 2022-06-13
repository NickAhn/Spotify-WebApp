from os import access
import pandas as pd
from flask import Flask, render_template, redirect, request, session
import spotify_auth
import json
import spotify_api

app = Flask(__name__)
app.config['TESTING'] = True

# data = main.getTopSongsData(SPOTIFY_API.getUserTopItems("short_term"))
# df = pd.DataFrame.from_dict(data['tracks'])
# df.index = df.index+1

# headings = df.columns.values
# data = df.values

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    # return render_template("main.html", columns=df.columns.values, rows=df.values.tolist())
    api = spotify_api.api()
    api.refreshAccessToken()
    return render_template("main.html", user=api.getCurrentUserProfile()['display_name'])


# -------------------- auth -------------------------
@app.route("/auth")
def auth():
    AUTH_URL = spotify_auth.requestUserAuthorization()
    print(AUTH_URL)
    return redirect(AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    access_token, refresh_token = spotify_auth.getAccessToken(auth_token)
    # session['token'] = access_token
    token = access_token

    f = open('secrets.json', 'r')
    data = json.load(f)
    data['access_token'] = access_token
    data['refresh_token'] = refresh_token

    f = open('secrets.json', 'w')
    f.write(json.dumps(data, indent=4))

    return render_template("index.html")
# ----------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=spotify_auth.PORT)