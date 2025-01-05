import pandas as pd
import os


def get_dj_show_info(dj_id):
    # Read in the data from the show responses Excel file
    show_responses_path = os.path.join(os.getcwd(), 'data', 'kxsc_fall24_show_responses.xlsx')
    responses = pd.read_excel(show_responses_path, engine='openpyxl')

    # All tracks played on KXSC
    tracks_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'sliced_ab_data.csv'))

    show_info = {
        'show_name': get_show_name(dj_id, responses),
        'timeslot': get_timeslot(dj_id, responses),
        'about_me': get_about_me(dj_id, responses),
        'mission_statement': get_mission_statement(dj_id, responses),
        'recent_songs': get_recent_songs(dj_id, tracks_df)
    }

    return show_info


def get_show_name(dj_id, responses):
    # Show name
    try:
        show_name = responses.loc[responses['DJ ID'] == dj_id, 'Name of your show'].iloc[0]
        if pd.isna(show_name):
            raise ValueError('Show Name is missing')
    except Exception as e:
        show_name = 'DJ Setlist'

    show_name = show_name.strip()
    return show_name


def get_timeslot(dj_id, responses):
    # Timeslot
    try:
        timeslot = responses.loc[responses['DJ ID'] == dj_id, 'Timeslot'].iloc[0]
        if pd.isna(timeslot):
            raise ValueError('Timeslot is missing')
    except Exception as e:
        timeslot = "See this DJ's time"

    timeslot = timeslot.strip()
    return timeslot


def get_about_me(dj_id, responses):
    # About me
    try:
        about_me = responses.loc[responses['DJ ID'] == dj_id, 'About Show'].iloc[0]
        if pd.isna(about_me):
            raise ValueError('About Me is missing')
    except Exception as e:
        about_me = 'This DJ does not have any About Show'

    about_me = about_me.strip()
    return about_me


def get_mission_statement(dj_id, responses):
    # Mission statement
    try:
        mission_statement = responses.loc[responses['DJ ID'] == dj_id, 'Mission Statement'].iloc[0]
        if pd.isna(mission_statement):
            raise ValueError('Mission Statement is missing')
    except Exception as e:
        mission_statement = 'No mission statement'

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


