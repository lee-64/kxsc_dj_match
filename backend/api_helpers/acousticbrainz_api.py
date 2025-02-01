import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv
import json

load_dotenv()
ab_base_url = os.getenv('AB_BASE_URL')
headers = json.loads(os.getenv('AB_HEADERS'))
rate_delay = float(os.getenv('AB_RATE_DELAY'))


def get_feature_data(row: pd.Series) -> pd.Series:
    row_data = {
        'track_mbid': None,
        'key': None,
        'key_scale': None,
        'key_confidence': None,
        'danceability': None,
        'bpm': None,
        'instrumental': None,
        'instrumental_confidence': None,
        'gender': None,
        'gender_confidence': None,
        'danceable': None,
        'danceable_confidence': None,
        'tonal': None,
        'tonal_confidence': None,
        'timbre': None,
        'timbre_confidence': None,
        'electronic': None,
        'electronic_confidence': None,
        'party': None,
        'party_confidence': None,
        'aggressive': None,
        'aggressive_confidence': None,
        'acoustic': None,
        'acoustic_confidence': None,
        'happy': None,
        'happy_confidence': None,
        'sad': None,
        'sad_confidence': None,
        'relaxed': None,
        'relaxed_confidence': None,
        'gztan_model': None,
        'gztan_genre_confidence': None,
        'electronic_classification': None,
        'electronic_genre_confidence': None,
        'dortmund': None,
        'dortmund_genre_confidence': None,
        'rosamerica': None,
        'rosamerica_confidence': None
    }
    low_level_data = get_low_level_data(row)
    time.sleep(rate_delay)
    row_data.update(low_level_data)

    mbid = low_level_data.get('track_mbid', None)
    if mbid is not None:
        high_level_data = get_high_level_data(mbid)
        time.sleep(rate_delay)
        row_data.update(high_level_data)
        print(f'MBID {mbid}: Fetched row_data.')
    else:
        print(f'MBID {mbid}: Could not fetch row_data.')

    return pd.Series(row_data)


# Tries to fetch low-level AcousticBrainz API data for a given row
def get_low_level_data(row: pd.Series):
    track_id = row['track_mbid']

    r = {}
    ab_low_level_url = f'{ab_base_url}/api/v1/{track_id}/low-level'

    try:
        response = requests.get(ab_low_level_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        r = response.json()

    except requests.HTTPError as http_err:
        print(f"Low-level request failed for MBID: {track_id}. Error: {http_err}")

        # Too many API calls
        status_code = response.status_code
        if status_code in [503, 429]:
            # Add an extra delay
            time.sleep(rate_delay)

    # Handle non-HTTP errors
    except requests.RequestException as e:
        print(f"Request failed for MBID: {track_id}. Error: {e}. Error not for retrying.")

    # A response with low-level data was found
    if r:
        try:
            key = r['tonal']['key_key']
            key_scale = r['tonal']['key_scale']
            key_confidence = r['tonal']['key_strength']
            danceability = r['rhythm']['danceability']
            bpm = int(round(r['rhythm']['bpm']))
        except KeyError as e:
            return {
                'track_mbid': None,
                'key': None,
                'key_scale': None,
                'key_confidence': None,
                'danceability': None,
                'bpm': None
            }
        return {
            'track_mbid': track_id,
            'key': key,
            'key_scale': key_scale,
            'key_confidence': key_confidence,
            'danceability': danceability,
            'bpm': bpm
        }

    # No response with low-level data was found from that song's MBIDs. This means that AcousticBrainz does not have audio feature data for this song.
    else:
        return {
            'track_mbid': None,
            'key': None,
            'key_scale': None,
            'key_confidence': None,
            'danceability': None,
            'bpm': None
        }


# Tries to fetch high-level AcousticBrainz API data for a given mbid (which had low-level data)
def get_high_level_data(track_mbid):
    ab_high_level_url = f'{ab_base_url}/api/v1/{track_mbid}/high-level'

    r = {}
    try:
        response = requests.get(ab_high_level_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        r = response.json()
    except requests.HTTPError as http_err:
        print(f"Low-level request failed for MBID: {track_mbid}. Error: {http_err}")

        # Too many API calls
        status_code = response.status_code
        if status_code in [503, 429]:
            # Add an extra delay
            time.sleep(rate_delay)

    # Handle non-HTTP errors
    except requests.RequestException as e:
        print(f"Request failed for MBID: {track_mbid}. Error: {e}. Error not for retrying.")

    # A response with high-level data was found
    if r:
        r = r['highlevel']
        if r['voice_instrumental']['value'] == 'instrumental':
            instrumental = 1
        else:
            instrumental = 0
        instrumental_confidence = r['voice_instrumental']['probability']
        if r['gender']['value'] == 'male':
            gender = 1  # Male
        else:
            gender = 0  # Female
        gender_confidence = r['gender']['probability']
        if r['danceability']['value'] == 'danceable':
            danceable = 1
        else:
            danceable = 0
        danceable_confidence = r['danceability']['probability']
        if r['tonal_atonal']['value'] == 'tonal':
            tonal = 1
        else:
            tonal = 0
        tonal_confidence = r['tonal_atonal']['probability']
        if r['timbre']['value'] == 'bright':
            timbre = 1
        else:
            timbre = 0
        timbre_confidence = r['timbre']['probability']

        # Moods
        if r['mood_electronic']['value'] == 'electronic':
            electronic = 1
        else:
            electronic = 0
        electronic_confidence = r['mood_electronic']['probability']
        if r['mood_party']['value'] == 'party':
            party = 1
        else:
            party = 0
        party_confidence = r['mood_party']['probability']
        if r['mood_aggressive']['value'] == 'aggressive':
            aggressive = 1
        else:
            aggressive = 0
        aggressive_confidence = r['mood_aggressive']['probability']
        if r['mood_acoustic']['value'] == 'acoustic':
            acoustic = 1
        else:
            acoustic = 0
        acoustic_confidence = r['mood_acoustic']['probability']
        if r['mood_happy']['value'] == 'happy':
            happy = 1
        else:
            happy = 0
        happy_confidence = r['mood_happy']['probability']
        if r['mood_sad']['value'] == 'sad':
            sad = 1
        else:
            sad = 0
        sad_confidence = r['mood_sad']['probability']
        if r['mood_relaxed']['value'] == 'relaxed':
            relaxed = 1
        else:
            relaxed = 0
        relaxed_confidence = r['mood_relaxed']['probability']

        # Genre Clustering
        gztan_model = r['genre_tzanetakis']['value']
        gztan_genre_confidence = r['genre_tzanetakis']['probability']
        electronic_classification = r['genre_electronic']['value']
        electronic_genre_confidence = r['genre_electronic']['probability']
        dortmund = r['genre_dortmund']['value']
        dortmund_genre_confidence = r['genre_dortmund']['probability']
        rosamerica = r['genre_rosamerica']['value']
        rosamerica_confidence = r['genre_rosamerica']['probability']

        return {
            'instrumental': instrumental,
            'instrumental_confidence': instrumental_confidence,
            'gender': gender,
            'gender_confidence': gender_confidence,
            'danceable': danceable,
            'danceable_confidence': danceable_confidence,
            'tonal': tonal,
            'tonal_confidence': tonal_confidence,
            'timbre': timbre,
            'timbre_confidence': timbre_confidence,
            'electronic': electronic,
            'electronic_confidence': electronic_confidence,
            'party': party,
            'party_confidence': party_confidence,
            'aggressive': aggressive,
            'aggressive_confidence': aggressive_confidence,
            'acoustic': acoustic,
            'acoustic_confidence': acoustic_confidence,
            'happy': happy,
            'happy_confidence': happy_confidence,
            'sad': sad,
            'sad_confidence': sad_confidence,
            'relaxed': relaxed,
            'relaxed_confidence': relaxed_confidence,
            'gztan_model': gztan_model,
            'gztan_genre_confidence': gztan_genre_confidence,
            'electronic_classification': electronic_classification,
            'electronic_genre_confidence': electronic_genre_confidence,
            'dortmund': dortmund,
            'dortmund_genre_confidence': dortmund_genre_confidence,
            'rosamerica': rosamerica,
            'rosamerica_confidence': rosamerica_confidence
        }

    # No response with high-level data was found from that song's MBIDs. This means that AcousticBrainz does not have
    # audio feature data for this track.
    else:
        return {
            'instrumental': None,
            'instrumental_confidence': None,
            'gender': None,
            'gender_confidence': None,
            'danceable': None,
            'danceable_confidence': None,
            'tonal': None,
            'tonal_confidence': None,
            'timbre': None,
            'timbre_confidence': None,
            'electronic': None,
            'electronic_confidence': None,
            'party': None,
            'party_confidence': None,
            'aggressive': None,
            'aggressive_confidence': None,
            'acoustic': None,
            'acoustic_confidence': None,
            'happy': None,
            'happy_confidence': None,
            'sad': None,
            'sad_confidence': None,
            'relaxed': None,
            'relaxed_confidence': None,
            'gztan_model': None,
            'gztan_genre_confidence': None,
            'electronic_classification': None,
            'electronic_genre_confidence': None,
            'dortmund': None,
            'dortmund_genre_confidence': None,
            'rosamerica': None,
            'rosamerica_confidence': None
        }
