import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import cred
from flask import Flask, request, url_for, session, redirect, jsonify
from userAuth import *


app = Flask(__name__)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdfklasjfd;as234234j2w$%##'
TOKEN_INFO = 'token_info'

redirect_url = 'https://www.google.com/?client=safari'

scope = "user-read-recently-played user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope))


@app.route('/testing')
def testing():
    return ({"testingtesting": ['1','2','3']})

# uses args "n"
@app.route('/getRecentTracks')
def recent_tracks():
    n_tracks = request.args.get('n')
    results = get_recent_tracks(sp, n_tracks)
    return jsonify(get_from_tracks(sp, results, get_ids=False, get_dates=True, get_names=True, get_artists=True, get_album_arts=True, get_lyrics_bool=True))

# uses args "n" and "time_range" e.g., "http://127.0.0.1:5000/getTopTracks?n=10&time_range=long_term"
@app.route('/getTopTracks')
def top_tracks():
    n_tracks = request.args.get('n')
    time_range = request.args.get('time_range')
    results = get_top_tracks(sp, n_tracks, time_range)
    return jsonify(get_from_tracks(sp, results, get_ids=False, get_dates=False, get_names=True, get_artists=True, get_album_arts=True, get_lyrics_bool=True))
    
# uses args "n" and "time_range" e.g., "http://127.0.0.1:5000/getTopArtists?n=10&time_range=long_term"
@app.route('/getTopArtists')
def top_artists():
    n_artists = request.args.get('n')
    time_range = request.args.get('time_range')
    results = get_top_artists(sp, n_artists, time_range)
    return jsonify(get_artist_images_and_names(sp, results))

@app.route('/savedData')
def saved_data():
    try: 
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        return redirect('/')
    return("OAUTH SUCCESSFUL")

@app.route('/generatePlaylist')
def generate_playlist():
    query = request.args.get('query')
    return jsonify(get_playlist_by_query(query))
    

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    # if not token_info:
    #     redirect(url_for('login'))
    
    # now = int(time.time())

    # is_expired = token_info['expires_at'] - now < 60

    # if (is_expired):
    #     spotify_oauth = create_Spotify_OAuth
    #     token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_Spotify_OAuth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:5000/redirect",
        scope='user-library-read'
    )

app.run(debug=True)
