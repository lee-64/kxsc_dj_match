import musicbrainzngs
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize MusicBrainz
musicbrainzngs.set_useragent(os.getenv('MB_APP'), os.getenv('MB_VER'), os.getenv('MB_CONTACT'))


def get_track_id(artist_mbid, track_name):
    """
    Search for a track in MusicBrainz by artist MBID and track name.
    Returns the MusicBrainz Recording ID if found, else None.
    """
    try:
        result = musicbrainzngs.search_recordings(artist=artist_mbid, recording=track_name, limit=1)
        recordings = result.get('recording-list', [])
        if recordings:
            recording = recordings[0]
            print(f"Found MusicBrainz Track: {recording['title']} (MBID: {recording['id']})")
            return recording['id']
        else:
            print(f"No MusicBrainz Track ID found for '{track_name}'.")
            return None
    except musicbrainzngs.WebServiceError as e:
        print(f"MusicBrainz error while searching for '{track_name}': {e}")
        return None
