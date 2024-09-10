# from flask import Flask, request, url_for, session, redirect
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import cred
import lyricsgenius as lg

# from requests import post
# from requests import get
# import time

def get_lyricsgenius_object(token):
    ### LYRICSGENIUS OAUTH IS BROKEN AS NOTED ON THEIR GITHUB ###
    ### INSTEAD WE CAN USE MY PERSONAL TOKEN ###
    # client_id = lyricsgenius_client_id
    # redirect_uri = lyricsgenius_redirect_uri
    # auth = lg.OAuth2.client_only_app(client_id, redirect_uri)
    # token = auth.prompt_user()
    # token = "PPJGxZslw279AmNttc05MCgFBACyaF1wG7VBETI5VMPz1QmvTSHp1afTEFaAIikL"
    genius = lg.Genius(token)
    return genius

# returns results from API for use in get functions for recent tracks
def get_recent_tracks(sp_login, n_tracks):
    return sp_login.current_user_recently_played(limit=n_tracks)

# returns results from API for use in get functions for top tracks
def get_top_tracks(sp_login, n_tracks, time_range="long_term"):
    return sp_login.current_user_top_tracks(limit=n_tracks, time_range=time_range)

# returns resutls from API for us in get functions for top artists
def get_top_artists(sp_login, n_artists, time_range="long_term"):
    return sp_login.current_user_top_artists(limit=n_artists, time_range=time_range)


# returns track_ids given a list of tracks (usually from results["items"])
def get_track_id(tracks):
    track_ids = []
  
    for item in tracks:
        if "track" in item.keys():
            track_ids.append(item['track']['id'])
        else:
            track_ids.append(item['id'])

    return track_ids

# returns dates tracks were played given a list of tracks (usually from results["items"])
def get_date_played(tracks):
    dates_played = []
    for item in tracks:
        if "played_at" not in item.keys():
            dates_played.append(False)
        else:
            dates_played.append(item['played_at'])

    return dates_played

# returns track_names (a list of track/song names) given a list of tracks (usually from results["items"])
def get_track_name(tracks):
    track_names = []
    for item in tracks:
        if "track" in item.keys():
            track_names.append(item['track']['name'])
        else:
            track_names.append(item['name'])
    return track_names

def get_artist_name(tracks):
    # print(tracks[0]["artists"])
    artist_names = []
    for item in tracks:
        if "track" in item.keys():
            artist_names.append(item['track']['artists'][0]["name"])
        else:
            artist_names.append(item['artists'][0]["name"])
    return artist_names

def get_artist_image(tracks):
    artist_images = []
    for item in tracks:
        if "track" in item.keys():
            artist_images.append(item['track']["images"][1])
        else:
            artist_images.append(item["images"][1])
    return artist_images
            
    
def get_album_art(tracks):
    album_arts = []
    for item in tracks:
        if "track" in item.keys():
            album_arts.append(item['track']['album']['images'])
        else:
            album_arts.append(item['album']['images'])
    return album_arts


def get_lyrics_from_song(song_title, song_artist):
    song = lyricsgenius_object.search_song(song_title, song_artist)
    if song is None:
        return "No Lyrics Found"
    s = song.to_dict()["lyrics"].split("Lyrics")[1][:-5]
    
    while s[-1].isnumeric():
        s = s[:-1]
        
    return s


def get_lyrics(tracks):
    lyrics = []
    queries = zip(get_track_name(tracks), get_artist_name(tracks))
    for title, artist in queries:
        lyrics.append(get_lyrics_from_song(title, artist))
    return lyrics
    

# returns whatever is needed in one traversal
def get_from_tracks(sp_login, results, get_ids=True, get_dates=False, get_names=False, get_artists=False, get_album_arts=False, get_lyrics_bool=False):
    n_tracks = len(results)

    if get_ids:
        track_ids = get_track_id(results['items'])
    if get_dates:
        dates = get_date_played(results['items'])
    if get_names or get_lyrics_bool:
        names = get_track_name(results['items'])
    if get_artists or get_lyrics_bool:
        artists = get_artist_name(results['items'])
    if get_album_arts:
        album_arts = get_album_art(results['items'])

    while results['next'] and len(results) < n_tracks:
        results = sp_login.next(results)
        if get_ids:
            track_ids.extend(get_track_id(results['items']))
        if get_dates:
            dates.extend(get_date_played(results['items']))
        if get_names or get_lyrics_bool:
            names.extend(get_track_name(results['items']))
        if get_artists or get_lyrics_bool:
            artists.extend(get_artist_name(results['items']))
        if get_album_arts:
            album_arts.extend(get_album_art(results['items']))
        
    if get_lyrics_bool:
        lyrics = []
        queries = zip(names, artists)
        for title, artist in queries:
            lyrics.append(get_lyrics_from_song(title, artist))

    requested_data = {}
    if get_ids:
        requested_data["Ids"] = track_ids
    if get_dates:
        requested_data["Dates"] = dates
    if get_names:
        requested_data["Song Titles"] = names
    if get_artists:
        requested_data["Artists"] = artists
    if get_album_arts:
        requested_data["Album Art"] = album_arts
    if get_lyrics_bool:
        requested_data["Lyrics"] = lyrics
    if len(requested_data) == 1:
        return list(requested_data.values())[0]
    
    return requested_data

def get_track_ids_from_tracks(sp_login, results):
    n_tracks = len(results)
    track_ids = get_track_id(results['items'])
    while results['next'] and len(results) < n_tracks:
        results = sp_login.next(results)
        track_ids.extend(get_track_id(results['items']))
    return track_ids

def get_names_from_tracks(sp_login, results):
    n_tracks = len(results)
    names = get_track_name(results['items'])
    while results['next'] and len(results) < n_tracks:
        results = sp_login.next(results)
        names.extend(get_track_name(results['items']))
    return names


def get_date_played_from_tracks(sp_login, results):
    n_tracks = len(results)
    dates = get_date_played(results['items'])
    while results['next'] and len(results) < n_tracks:
        results = sp_login.next(results)
        dates.extend(get_date_played(results['items']))
    return dates

def get_playlist_by_query(query):
    result = sp.search(q=query, type="playlist", limit=10)
    playlists = result['playlists']['items']
    songs_to_add = []
    
    for item in playlists:
        tracks = sp.playlist_items(item['id'], limit=5)
        for track_item in tracks['items']:
            track_uri = track_item['track']['id']
            songs_to_add.append(track_uri)

    name = "Generated Playlist: " + query
    returnVal = sp.user_playlist_create(sp.current_user()['id'], name, public=True, description='')
    id = returnVal['id']

    formatted_songs_to_add = []
    for x in songs_to_add:
        formatted_songs_to_add.append(x)

    sp.user_playlist_add_tracks(sp.current_user()['id'], id, formatted_songs_to_add, position=None)
    return sp.playlist_cover_image(id)


def get_lyrics_from_tracks(sp_login, results):
    n_tracks = len(results)
    lyrics = get_lyrics(results['items'])
    while results['next'] and len(results) < n_tracks:
        results = sp_login.next(results)
        lyrics.extend(get_lyrics(results['items']))
    return lyrics   

def get_names_from_artists(sp_login, results):
    n_artists = len(results)
    names = get_track_name(results['items'])
    while results['next'] and len(results) < n_artists:
        results = sp_login.next(results)
        names.extend(get_track_name(results['items']))
    return names

def get_images_from_artists(sp_login, results):
    n_artists = len(results)
    images = get_artist_image(results['items'])
    while results['next'] and len(results) < n_artists:
        results = sp_login.next(results)
        images.extend(get_artist_image(results['items']))
    return images

def get_artist_images_and_names(sp_login, results):
    return {"Artists":get_names_from_artists(sp_login, results), "Images":get_images_from_artists(sp_login, results)}

load_dotenv()

# client_id = '554ff56e30bf482ca5b9b6afbe71fc1d'
client_id = os.getenv("CLIENT_ID")
# client_secret = '7e8b02ce9bcc49cfa790b220d980cb84'
client_secret = os.getenv("CLIENT_SECRET")
# NOTE: make sure this redirect URL is listed on your Spotify API page
redirect_url = 'https://www.google.com/?client=safari'

scope = "user-read-recently-played user-top-read playlist-modify-public"
lyricsgenius_token = os.getenv("GENIUS_CLIENT_TOKEN")
lyricsgenius_object = get_lyricsgenius_object(lyricsgenius_token)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope))