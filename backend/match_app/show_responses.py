import pandas as pd
import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('MONGO_CONNECTION_URI')


def get_dj_show_info(dj_id):
    dj_id = int(dj_id)  # Cast dj_id from numpy.int64 to an int

    # Read in the data from the show responses Excel file
    client = MongoClient(uri)
    db = client['djs']
    collection = db['show_responses']

    # All tracks played on KXSC
    tracks_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'sliced_ab_data.csv'))

    show_info = {
        'show_name': get_show_name(dj_id, collection),
        'timeslot': get_timeslot(dj_id, collection),
        'about_me': get_about_me(dj_id, collection),
        'mission_statement': get_mission_statement(dj_id, collection),
        'recent_songs': get_recent_songs(dj_id, tracks_df)
    }

    client.close()
    return show_info


def get_show_name(dj_id, responses):
    # Show name
    try:
        show_name = responses.find_one({'DJ ID': dj_id})['Name of your show']
        if pd.isna(show_name):
            raise ValueError('Show Name is missing')
    except Exception as e:
        show_name = 'DJ Setlist'

    show_name = show_name.strip()
    return show_name


def get_timeslot(dj_id, responses):
    # Timeslot
    try:
        timeslot = responses.find_one({'DJ ID': dj_id})['Timeslot']
        if pd.isna(timeslot):
            raise ValueError('Timeslot is missing')
    except Exception as e:
        timeslot = "See this DJ's time"  # ... at kxsc.org

    timeslot = timeslot.strip()
    return timeslot


def get_about_me(dj_id, responses):
    # About me
    try:
        about_me = responses.find_one({'DJ ID': dj_id})['About Show']
        if pd.isna(about_me):
            raise ValueError('About Me is missing')
    except Exception as e:
        about_me = 'This DJ does not have an About section.'

    about_me = about_me.strip()
    return about_me


def get_mission_statement(dj_id, responses):
    # Mission statement
    try:
        mission_statement = responses.find_one({'DJ ID': dj_id})['Mission Statement']
        if pd.isna(mission_statement):
            raise ValueError('Mission Statement is missing')
    except Exception as e:
        mission_statement = 'No mission statement.'

    mission_statement = mission_statement.strip()
    return mission_statement


def get_recent_songs(dj_id, tracks_df):
    n = 5  # DJ's 5 most recently played songs

    tracks_df['Date'] = pd.to_datetime(tracks_df['Date'])
    tracks_df['Time'] = pd.to_datetime(tracks_df['Time'], format='%I:%M:%S %p').dt.time
    tracks_df.sort_values(by=['Date', 'Time'], ascending=False, inplace=True)

    recent_artists = tracks_df[tracks_df['DJ ID'] == dj_id]['Artist'].head(5).to_list()
    recent_song_names = tracks_df[tracks_df['DJ ID'] == dj_id]['Song'].head(5).to_list()

    # Formatted as "Song Name - Artist Name"
    recent_songs = []
    for song, artist in zip(recent_song_names, recent_artists):
        song = song.strip()
        artist = artist.strip()
        recent_songs.append(song + ' - ' + artist)

    return recent_songs


