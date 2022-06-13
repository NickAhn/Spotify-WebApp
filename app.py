# import main
# from main import SPOTIFY_API
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
app.config['TESTING'] = True

# data = main.getTopSongsData(SPOTIFY_API.getUserTopItems("short_term"))
# df = pd.DataFrame.from_dict(data['tracks'])
# df.index = df.index+1

headings = ("Title", "Artist")
data = ()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/table", methods=("POST", "GET"))
def table():
    return render_template("table.html")

