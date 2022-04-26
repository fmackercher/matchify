from flask import Flask, render_template, redirect, request, session, make_response, session, redirect
import requests
import spotipy
import spotipy.util as util
import time
import json
from secrets import CLIENT_ID, CLIENT_SECRET
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.secret_key = 'matchify'

API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI = "http://127.0.0.1:5000/callback"

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

# Set this to True for testing but you probaly want it set to False in production.
SHOW_DIALOG = True


# authorization-code-flow Step 1. Have your application request authorization;
# the user logs in and authorizes access
@app.route("/")
def verify():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    # sp_oauth = spotipy.oauth2.SpotifyOAuth(
    #     client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    # auth_url = sp_oauth.get_authorize_url()
    auth_url = f'{API_BASE}/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)


@app.route("/index")
def index():
    return render_template("index.html")

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens


@app.route("/callback")
def callback():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    # sp_oauth = spotipy.oauth2.SpotifyOAuth(
    #     client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    # session.clear()
    # code = request.args.get('code')
    # token_info = sp_oauth.get_access_token(code)

    # # Saving the access token along with all other token related info
    # session["token_info"] = token_info
    session.clear()
    code = request.args.get('code')

    auth_token_url = f'{API_BASE}/api/token'
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/callback",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    res_body = res.json()
    print(res_body)
    session['toke'] = res_body.get('access_token')

    return redirect("index")

# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data


def getUserInfo():
    data = request.form
    sp = spotipy.Spotify(auth=session['toke'])
    response = sp.current_user()
    print(response)
    return response


def getTopArtistsShort():
    data = request.form
    sp = spotipy.Spotify(auth=session['toke'])
    response = sp.current_user_top_artists(
        limit=10, offset=0, time_range='short_term')['items']
    # print(response)
    return response


def getTopArtistsMedium():
    data = request.form
    sp = spotipy.Spotify(auth=session['toke'])
    response = sp.current_user_top_artists(
        limit=10, offset=0, time_range='medium_term')['items']
    # print(response)
    return response


def getTopArtistsLong():
    data = request.form
    sp = spotipy.Spotify(auth=session['toke'])
    response = sp.current_user_top_artists(
        limit=10, offset=0, time_range='long_term')['items']
    # print(response)
    return response


@app.route('/artists')
def artists():
    # sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # response = (sp.current_user_top_artists(
    #     limit=20, offset=0, time_range='medium_term'))['items']
    # app.logger.info(response)
    user_info = getUserInfo()
    name = user_info['display_name']
    data1 = getTopArtistsShort()
    top_artists_short = []
    for artist in data1:
        top_artists_short.append(artist['name'])
    print(top_artists_short)
    data2 = getTopArtistsMedium()
    top_artists_medium = []
    for artist in data2:
        top_artists_medium.append(artist['name'])
    print(top_artists_medium)
    data3 = getTopArtistsLong()
    top_artists_long = []
    for artist in data3:
        top_artists_long.append(artist['name'])
    print(top_artists_long)
    return render_template('artists.html', name=name, data1=top_artists_short, data2=top_artists_medium, data3=top_artists_long)


@app.route('/blender/form', methods=['POST'])
def form_post():
    text = request.form['text']
    return text


@app.route('/blender')
def blender():
    return render_template('blender.html')


if __name__ == "__main__":
    app.run(debug=True)
