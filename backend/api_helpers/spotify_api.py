import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Initialize Spotipy with Client Credentials Manager
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_artist_id(artist_name):
    """
    Search for the artist on Spotify and return their Spotify Artist ID.
    """
    # TODO Explicitly grab most popular result
    results = sp.search(q=artist_name, type='artist', limit=1)
    items = results['artists']['items']
    if not items:
        raise Exception(f"No artist found on Spotify with name '{artist_name}'.")
    artist = items[0]
    print(f"Found Spotify Artist: {artist['name']} (ID: {artist['id']})")
    return artist['id'], artist['name']


def get_top_tracks(artist_id, country='US', limit=3):
    """
    Retrieve the top tracks for a given Spotify Artist ID.
    """
    results = sp.artist_top_tracks(artist_id, country=country)
    tracks = results['tracks'][:limit]
    top_tracks = []
    for track in tracks:
        track_info = {
            'name': track['name'],
            'spotify_track_id': track['id'],
            'spotify_popularity': track['popularity']
        }
        top_tracks.append(track_info)

    return top_tracks
