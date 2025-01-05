class DJ:
    def __init__(self, dj_id, tracks_df):
        self.dj_id = dj_id
        self.tracks = tracks_df[tracks_df['DJ ID'] == dj_id]
        self.avg_features = self.calculate_avg_features()

    def calculate_avg_features(self):
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

        # TODO explore the differences in accuracy between Probabilistic Score and Weighted Average
        # Currently this is Probabilistic Score
        tracks_prob = calculate_probabilistic_scores(self.tracks, binary_feature_cols, confidence_feature_cols)
        prob_cols = [col for col in tracks_prob.columns if col.endswith('_prob')]
        cols_to_average = misc_feature_cols + prob_cols

        avg_features = tracks_prob[cols_to_average].mean().to_numpy()

        return avg_features

    def get_name(self):
        name = self.tracks['DJ Name'].iloc[0]
        return name

    def get_id(self):
        return self.dj_id

    def get_tracks(self):
        return self.tracks


def calculate_probabilistic_scores(df, binary_features, confidence_features):
    df_prob = df.copy()

    for binary, confidence, in zip(binary_features, confidence_features):
        prob_col = f'{binary}_prob'
        df_prob[prob_col] = (df_prob[binary] * df_prob[confidence]) + ((1 - df_prob[binary]) * (1 - df_prob[confidence]))

    return df_prob
