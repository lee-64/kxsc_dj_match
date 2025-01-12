import pandas as pd
import numpy as np
import os
import math
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from .user import User
from .dj import DJ


def get_matches(mood, user_artists, user_tracks):
    tracks_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'sliced_ab_data.csv'))

    # TODO future version: include the genres and key major/minor as dummies in calculation

    # Initialize DJs
    djs_list = []
    unique_dj_ids = tracks_df['DJ ID'].unique()
    for dj_id in unique_dj_ids:
        djs_list.append(DJ(dj_id, tracks_df))

    dj_matrix = np.stack([dj.avg_features for dj in djs_list])  # shape: (num_djs, num_features)

    user = User(mood, user_artists, [], tracks_df)
    user_vector = user.avg_features.reshape(1, -1)  # shape: (1, num_features)

    # Initialize and fit the StandardScaler on DJ data only
    scaler = StandardScaler()
    scaler.fit(dj_matrix)

    # Transform both DJ and User vectors using the same scaler
    dj_scaled_matrix = scaler.transform(dj_matrix)
    user_scaled_vector = scaler.transform(user_vector)

    # TODO if user_vector contains some NA values (eg high-level data get didnt work), cosine similarity will throw error
    feature_similarities = cosine_similarity(user_scaled_vector, dj_scaled_matrix).flatten()  # shape: (num_djs, )

    # TODO Include "same song matches" and "same artist" matches in the calculation. Use song NAME instead of mbid alongside artist_mbid, since there can be multiple mbids for one song (but generally only 1 artist_mbid).
    # Calculate artist overlap scores with frequency weighting
    artist_overlap_scores = np.zeros(len(djs_list))
    for i, dj in enumerate(djs_list):
        # Count frequency of each artist played by DJ
        dj_artist_frequencies = dj.get_tracks()['artist_id'].value_counts()

        user_artists_ids = {artist['mbid'] for artist in user_artists}

        # Calculate weighted overlap
        weighted_overlap = 0
        for artist_id in user_artists_ids:
            if artist_id in dj_artist_frequencies.index:
                # Add normalized frequency for each matching artist
                # Log scale to prevent extremely frequent plays from dominating
                weighted_overlap += np.log1p(dj_artist_frequencies[artist_id])

        # Normalize by number of user artists and max possible frequency
        max_possible_freq = np.log1p(dj.get_tracks()['artist_id'].value_counts().max())
        artist_overlap_scores[i] = (weighted_overlap / (len(user_artists_ids) * max_possible_freq)) if user_artists_ids else 0

    # Combine feature similarity and artist overlap with weights
    alpha = 0.85  # Feature similarity weight
    beta = 0.15   # Artist overlap weight

    overall_scores = (alpha * feature_similarities + beta * artist_overlap_scores)


    # TODO Add genre similarity, much like how users can select a Mood

    # TODO Angular Similarity for further spacing between the top 5 dj matches
    # ang_similarities = angular_similarity(cos_similarities)

    top_n = 5
    top_n_indices = overall_scores.argsort()[-top_n:][::-1]  # Sort in desc order + pick best n

    matched_djs = [
        {
            'dj_name': djs_list[idx].get_name(),
            'dj_id': djs_list[idx].get_id(),
            'similarity': feature_similarities[idx],
            # Linear map cosine sim from [-1, 1] -> [0, 100], then round
            'match_percent': round(((overall_scores[idx] + 1) / 2) * 100, 2),
        }
        for i, idx in enumerate(top_n_indices)
    ]

    print(matched_djs)

    # The features array (identical to dj.avg_features) of the top DJ match, used for visualization purposes
    match_features = dj_scaled_matrix[top_n_indices][0]
    user_features = user_scaled_vector.flatten()

    return matched_djs, match_features, user_features


def calculate_artist_overlap_score(user_artists, dj_artists):
    common_artists = len(set(user_artists) & set(dj_artists))
    total_user_artists = len(user_artists)
    # Normalize the score between 0 and 1
    overlap_score = common_artists / total_user_artists if total_user_artists > 0 else 0
    return overlap_score


def angular_similarity(cos_sim):
    """
    Computes an angular similarity matrix from a cosine similarity matrix.
    :param cos_sim: The cosine similarity matrix returned from scikit-learn cosine_similarity()
    :return: The angular similarity matrix.
    """
    return 1 - math.acos(cos_sim) / math.pi


def spider_plot(user_vector, dj_vector, dj_name):
    # Feature column names from user_vector and dj_vector
    angular_vars = ['danceability', 'bpm', 'instrumental_prob', 'gender_prob', 'tonal_prob', 'timbre_prob', 'electronic_prob', 'party_prob', 'aggressive_prob', 'acoustic_prob', 'happy_prob', 'sad_prob', 'relaxed_prob']

    # Rename columns to look prettier
    angular_vars = prettify_theta(angular_vars)

    # Remove the 'Danceability Probability/Confidence' feature from the visualization. While it is useful in the
    # calculations (as a Danceable yes/no likelihood metric), its difference from the 'Danceability' feature (which is a
    # low-level, rather than a high-level, AcousticBrainz feature and therefore more accurate) is too nuanced to explain
    # in a big-picture feature data visualization. However, they are similar enough that its exclusion should not cloud
    # any conclusions the user might draw.
    # So, 'Danceability Probability/Confidence' located at index i=4 is removed from the visualization only.
    user_vector_mod = np.delete(user_vector, 4)
    dj_vector_mod = np.delete(dj_vector, 4)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=user_vector_mod,
        theta=angular_vars,
        fill='toself',
        name='You'
    ))

    fig.add_trace(go.Scatterpolar(
        r=dj_vector_mod,
        theta=angular_vars,
        fill='toself',
        name=dj_name
    ))

    # Disable drag and zoom
    fig.update_layout(
        dragmode=False,
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    # fig_json = pio.to_json(fig)
    fig_json = fig.to_json()

    return fig_json


def prettify_theta(column_names):
    # TODO only show the mood that the user selected
    name_mapping = {
        'danceability': 'Danceability',
        'bpm': 'Tempo',
        'instrumental_prob': 'Instrumentality',
        'gender_prob': 'Vocalist Type',
        'danceable_prob': 'Danceability Prob',
        'tonal_prob': 'Tonality',
        'timbre_prob': 'Timbre',
        'electronic_prob': 'Electronic Index',
        'party_prob': 'Party Index',
        'aggressive_prob': 'Aggressive Index',
        'acoustic_prob': 'Acoustic Index',
        'happy_prob': 'Happy Index',
        'sad_prob': 'Sad Index',
        'relaxed_prob': 'Relaxed Index'
    }

    renamed_cols = [name_mapping.get(col) for col in column_names]

    return renamed_cols
