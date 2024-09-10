import pytest
from userAuth import *

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
# NOTE: make sure this redirect URL is listed on your Spotify API page
redirect_url = 'https://www.google.com/?client=safari'

scope = "user-read-recently-played user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope))

track_nums_to_test = [5, 10, 50]

class TestGetSPLogin:
    def test_sp_login(self):
        assert client_id != None and client_id != "", "Client ID Error"
        assert client_secret != None and client_secret != "", "Client Secret Error"
        assert sp != None, "Login Failed"

    def test_simple_request(self):
        recently_played = sp.current_user_recently_played()
        assert "items" in recently_played, "Failed to Fetch Recently Played in Simple Request"
        
class TestRecentTracks:
    def test_get_recent_tracks(self):
        for num_tracks in track_nums_to_test:
            results = get_recent_tracks(sp, num_tracks)
            assert len(results) == 5, "GOT Incorrect Number of items in tracks (get_recent_tracks should have 5)"
        
    def test_get_recent_track_ids_recent(self):
        for num_tracks in track_nums_to_test:
            results = get_recent_tracks(sp, num_tracks)
            track_ids = get_track_ids_from_tracks(sp, results)
            assert len(track_ids) == num_tracks, "GOT Incorrect Number of Track Ids"
            for track_id in track_ids:
                assert len(track_id) == 22, "Track Id incorrect length" # this is seemingly standard for track ids
                
    def test_get_recent_track_names_recent(self):
        for num_tracks in track_nums_to_test:
            results = get_recent_tracks(sp, num_tracks)
            names = get_names_from_tracks(sp, results)
            assert len(names) == num_tracks, "GOT Incorrect Number of Track Names"
            for name in names:
                assert type(name) is str, "Name should be string"
                
    def test_get_date_played_from_tracks_recent(self):
        for num_tracks in track_nums_to_test:
            results = get_recent_tracks(sp, num_tracks)
            dates = get_date_played_from_tracks(sp, results)
            assert len(dates) == num_tracks, "GOT Incorrect Number of Track Dates"
            for date in dates:
                assert date != False
        
class TestTopTracks:
    def test_get_top_tracks(self):
        for num_tracks in track_nums_to_test:
            results = get_top_tracks(sp, num_tracks)
            assert len(results) == 7, "GOT Incorrect Number of items in tracks (get_top_tracks should have 7)"
        
    def test_get_recent_track_ids_top(self):
        for num_tracks in track_nums_to_test:
            results = get_top_tracks(sp, num_tracks)
            track_ids = get_track_ids_from_tracks(sp, results)
            assert len(track_ids) == num_tracks, "GOT Incorrect Number of Track Ids"
            for track_id in track_ids:
                assert len(track_id) == 22, "Track Id incorrect length" # this is seemingly standard for track ids
                
    def test_get_recent_track_names_top(self):
        for num_tracks in track_nums_to_test:
            results = get_top_tracks(sp, num_tracks)
            names = get_names_from_tracks(sp, results)
            assert len(names) == num_tracks, "GOT Incorrect Number of Track Names"
            for name in names:
                assert type(name) is str, "Name should be string"
                
    def test_get_date_played_from_tracks_top(self):
        for num_tracks in track_nums_to_test:
            results = get_top_tracks(sp, num_tracks)
            dates = get_date_played_from_tracks(sp, results)
            assert len(dates) == num_tracks, "GOT Incorrect Number of Track Dates"
            for date in dates:
                assert date == False, "Expected False instead of actual date" # return false if not right type of input
