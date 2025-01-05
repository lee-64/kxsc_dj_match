import pandas as pd
import numpy as np
import time
from api_helpers import spotify_api, musicbrainz_api
from data import acousticbrainz_db

pd.set_option('display.max_columns', None)


class User:
    def __init__(self, mood, artists, songs, tracks_df):
        self.mood = mood.lower()
        self.artists = artists
        self.songs = songs
        self.tracks_df = tracks_df
        self.avg_features = self.calculate_avg_features()

    def calculate_avg_features(self):
        avg_features = None
        user_df = self.create_user_df()

        # Toy dataframe for testing conditionals
        # user_df = pd.DataFrame({
        #     'track_mbid': ['440f60e8-0b25-4ec4-abb1-c6beec624ab0', '881ea822-c5b6-4c1e-b01d-ae2c058984d7', '16a6e0f5-87e2-4440-9d57-29903fc58c54', 'mbidwithna'],
        #     'relaxed': [1.0, 0.0, 1.0, np.nan],
        #     'danceability': [1.078721, 1.232888, 1.109746, np.nan],
        #     'bpm': [129.0, 165.0, 103.0, np.nan]
        # })
        # cols_to_average = ['relaxed', 'danceability', 'bpm']


        misc_feature_cols = ['danceability', 'bpm']
        binary_feature_cols = ['instrumental',
                               'gender',
                               'danceable',
                               'tonal',
                               'timbre',
                               'electronic',
                               'party',
                               'aggressive',
                               'acoustic',
                               'happy',
                               'sad',
                               'relaxed']

        confidence_feature_cols = ['instrumental_confidence',
                                   'gender_confidence',
                                   'danceable_confidence',
                                   'tonal_confidence',
                                   'timbre_confidence',
                                   'electronic_confidence',
                                   'party_confidence',
                                   'aggressive_confidence',
                                   'acoustic_confidence',
                                   'happy_confidence',
                                   'sad_confidence',
                                   'relaxed_confidence']



        # Apply mood transformation
        if self.mood is not None:
            print("mood:", self.mood)

            tracks_prob = calculate_probabilistic_scores(self.tracks_df, binary_feature_cols, confidence_feature_cols)
            prob_cols = [col for col in tracks_prob.columns if col.endswith('_prob')]
            feature_cols = misc_feature_cols + prob_cols

            # Filter for songs from the overall tracks DataFrame that have the desired mood
            mood_df = tracks_prob[tracks_prob[self.mood] == 1]
            # Calculate the average features vector of all tracks with the desired mood
            avg_mood_features = mood_df[feature_cols].mean().to_numpy()

            # If the user's DataFrame is empty, meaning the user added no artists or no AcousticBrainz data was found
            if user_df.dropna().empty:
                print('user_df.dropna() is empty')
                # TODO add noise so that it doesn't return the same DJ for "relaxed" every time
                return avg_mood_features

            user_prob = calculate_probabilistic_scores(user_df, binary_feature_cols, confidence_feature_cols)
            print("user_prob:", user_prob)

            # Filter for songs from the user's DataFrame that have the desired mood
            ######## user_mood_df = user_prob[user_prob[self.mood] == 1]


            # If there are no songs in the user's DataFrame that match their desired mood
            # if user_mood_df.empty:
            if user_prob.empty:
                print('user_mood_df is empty')
                # TODO add noise so that it doesn't return the same DJ for "relaxed" every time
                return avg_mood_features

            # Calculate the average features vector of the user's tracks with the desired mood
            # avg_user_features = user_mood_df[feature_cols].mean().to_numpy()
            avg_user_features = user_prob[feature_cols].mean().to_numpy()

            # If the user's DataFrame 'u_df' and the DataFrame of the user's filtered songs 'mood_u_df' are the same
            # i.e. every song in the user's DataFrame is the user's desired mood
            # if user_df.dropna().equals(user_mood_df):
            if user_df.dropna().equals(user_prob):
                print('filtered mood and its still the same!!')
                return avg_user_features

            # Apply the mood transformation
            else:
                alpha = 0.7  # Weight: 70% for global mood average, 30% for user mood average
                transformed_mood_features = alpha * avg_mood_features + (1 - alpha) * avg_user_features
                print('Transformed mood features!')
                return transformed_mood_features

        # TODO add return value if the user somehow didn't add a mood. technically not possible but just for completeness
        return ...

    def create_user_df(self):
        print('in user_df')
        u_df = pd.DataFrame()

        # Append any artists the user submitted
        if self.artists is not None:
            # Append artists' top 5 songs + the AcousticBrainz info
            artist_names = [artist['name'] for artist in self.artists]
            artist_mbids = [artist['mbid'] for artist in self.artists]

            artists_df = create_artists_df(artist_names, artist_mbids)

            # print(artists_df)
            # print("without na:", artists_df.dropna())

            u_df = artists_df.copy()



        # Append any songs the user submitted
        # if self.songs is not None:
        #     songs_df =


        u_df.dropna(inplace=True)
        return u_df


def create_artists_df(artist_names, artist_mbids):
    mb_tracks = []

    # Iterate through each artist the user inputted
    for name, mbid in zip(artist_names, artist_mbids):
        # Step 1: Get Spotify artist ID
        try:
            spotify_artist_id, spotify_artist_name = spotify_api.get_artist_id(name)
        except Exception as e:
            print(e)
            continue

        # Step 2: Get the Spotify artist_id's Top Tracks
        top_tracks = spotify_api.get_top_tracks(spotify_artist_id)
        print(f"\nTop {len(top_tracks)} Tracks for '{spotify_artist_name}':")
        for idx, track in enumerate(top_tracks, start=1):
            print(f"{idx}. {track['name']} (Popularity: {track['spotify_popularity']})")

        # Step 3: Search each track in MusicBrainz to get MBIDs
        print("\nSearching for MusicBrainz Track IDs...")
        for track in top_tracks:
            track_name = track['name']
            track_mbid = musicbrainz_api.get_track_id(mbid, track_name)
            if track_mbid:
                mb_tracks.append(
                    {
                        'artist': name,
                        'artist_mbid': mbid,
                        'track_name': track_name,
                        'track_mbid': track_mbid
                    }
                )

            # time.sleep(0.25)  # Rate limiting

    mb_df = pd.DataFrame(mb_tracks)

    # AcousticBrainz stuff
    if not mb_df.empty:
        ab_df = acousticbrainz_db.modify_ab_db(mb_df)



        return ab_df

    # TODO
    print('yet to be created else clause in create_artists_df')
    return ...


def calculate_probabilistic_scores(df, binary_features, confidence_features):
    df_prob = df.copy()

    for binary, confidence, in zip(binary_features, confidence_features):
        prob_col = f'{binary}_prob'
        df_prob[prob_col] = (df_prob[binary] * df_prob[confidence]) + ((1 - df_prob[binary]) * (1 - df_prob[confidence]))

    return df_prob



