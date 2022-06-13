from os import access
import main
from main import SPOTIFY_API
import pandas as pd
from flask import Flask, render_template, redirect, request, session
import spotify_auth

app = Flask(__name__)
app.config['TESTING'] = True

data = main.getTopSongsData(SPOTIFY_API.getUserTopItems("short_term"))
df = pd.DataFrame.from_dict(data['tracks'])
df.index = df.index+1

headings = df.columns.values
data = df.values

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html", columns=df.columns.values, rows=df.values.tolist())


# ------ auth ------------ 
@app.route("/auth")
def auth():
    AUTH_URL = spotify_auth.requestUserAuthorization()
    print(AUTH_URL)
    return redirect(AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    access_token, refresh_token = spotify_auth.getAccessToken(auth_token)
    # auth_header = spotify.authorize(auth_token)
    # session['auth_header'] = auth_header
    # print(auth_token)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=spotify_auth.PORT)