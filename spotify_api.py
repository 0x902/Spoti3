# spotify_api.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Spotify Authentication credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URL')

# Initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private"
))

def get_all_spotify_tracks(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id, fields="items(track(name,artists(name))),next")

    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            track_info = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']]
            }
            tracks.append(track_info)
        results = sp.next(results) if results['next'] else None

    return [{"title": track['name'], "artist": track['artists'][0]} for track in tracks]
