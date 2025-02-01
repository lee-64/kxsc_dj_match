import pandas as pd
import os
from .database_connection import get_db


def get_dj_show_info(dj_id):
    """
    Collects DJ's show details from database.

    :param dj_id: DJ's unique identifier
    :return: Dict containing show name, timeslot, about me, subtext, and recent songs
    """

    dj_id = int(dj_id)  # Cast dj_id from numpy.int64 to an int

    # Read in the data from the show responses collection
    # Get fresh connection
    client = get_db()
    db = client['djs']
    collection = db['show_responses']

    # All tracks played on KXSC
    tracks_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'sliced_ab_data.csv'))

    show_info = {
        'show_name': get_show_name(dj_id, collection),
        'timeslot': get_timeslot(dj_id, collection),
        'about_me': get_about_me(dj_id, collection),
        'subtext': get_subtext(dj_id, collection),
        'genres': get_genres(dj_id, collection),
        'recent_songs': get_recent_songs(dj_id, tracks_df)
    }

    client.close()
    return show_info


def get_show_name(dj_id, responses):
    """
    Fetches DJ's show name from responses collection.

    :param dj_id: DJ's unique identifier
    :param responses: MongoDB collection containing show info
    :return: String of DJ's show name
    """

    try:
        show_name = responses.find_one({'dj_id': dj_id})['show_name']
        if pd.isna(show_name):
            raise ValueError('Show Name is missing')
    except Exception as e:
        show_name = 'DJ Setlist'

    show_name = show_name.strip()
    return show_name


def get_timeslot(dj_id, responses):
    """
    Fetches DJ's timeslot from responses collection.

    :param dj_id: DJ's unique identifier
    :param responses: MongoDB collection containing show info
    :return: String of DJ's timeslot
    """

    try:
        timeslot = responses.find_one({'dj_id': dj_id})['timeslot']
        if pd.isna(timeslot):
            raise ValueError('Timeslot is missing')
    except Exception as e:
        timeslot = "See this DJ's time"  # ... at kxsc.org

    timeslot = timeslot.strip()
    return timeslot


def get_about_me(dj_id, responses):
    """
    Fetches DJ's about me from responses collection.

    :param dj_id: DJ's unique identifier
    :param responses: MongoDB collection containing show info
    :return: String of DJ's about me
    """

    try:
        about_me = responses.find_one({'dj_id': dj_id})['about_show']
        if pd.isna(about_me):
            raise ValueError('About me is missing')
    except Exception as e:
        about_me = 'This DJ does not have an about section.'

    about_me = about_me.strip()
    return about_me


def get_subtext(dj_id, responses):
    """
    Fetches DJ's subtext from responses collection.

    :param dj_id: DJ's unique identifier
    :param responses: MongoDB collection containing show info
    :return: String of DJ's subtext
    """

    try:
        subtext = responses.find_one({'dj_id': dj_id})['subtext'] # TODO update
        if pd.isna(subtext):
            raise ValueError('Subtext is missing')
    except Exception as e:
        subtext = 'NO SUBTEXT REPLACE'

    subtext = subtext.strip()
    return subtext


def get_genres(dj_id, responses):
    """
    Fetches DJ's genres from responses collection.

    :param dj_id: DJ's unique identifier
    :param responses: MongoDB collection containing show info
    :return: List of DJ's genres
    """

    try:
        genres_str = responses.find_one({'dj_id': dj_id})['genres']
        genres = genres_str.split(', ')
    except Exception as e:
        genres = []

    return genres


def get_recent_songs(dj_id, tracks_df):
    """
    Gets DJ's 5 most recently played songs in "Song - Artist" format.

    :param dj_id: DJ's unique identifier
    :param tracks_df: DataFrame containing KXSC track history
    :return: List of strings formatted as "Song Name - Artist Name"
    """

    n = 5  # DJ's 5 most recently played songs

    tracks_df['Date'] = pd.to_datetime(tracks_df['Date'])
    tracks_df['Time'] = pd.to_datetime(tracks_df['Time'], format='%I:%M:%S %p').dt.time
    tracks_df.sort_values(by=['Date', 'Time'], ascending=False, inplace=True)

    recent_artists = tracks_df[tracks_df['DJ ID'] == dj_id]['Artist'].head(n).to_list()
    recent_song_names = tracks_df[tracks_df['DJ ID'] == dj_id]['Song'].head(n).to_list()

    # Formatted as "Song Name - Artist Name"
    recent_songs = []
    for song, artist in zip(recent_song_names, recent_artists):
        song = song.strip()
        artist = artist.strip()
        recent_songs.append(song + ' - ' + artist)

    return recent_songs
