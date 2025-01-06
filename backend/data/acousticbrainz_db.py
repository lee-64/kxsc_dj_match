import pandas as pd
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from api_helpers import acousticbrainz_api
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('MONGO_CONNECTION_URI')


def get_connection():
    client = MongoClient(uri)
    db = client['users']
    collection = db['searched_ab_tracks']
    return client, collection


def modify_ab_db(mb_df):
    client, collection = get_connection()
    try:
        unique_track_ids = mb_df['track_mbid'].unique()

        # Get existing data
        existing_ab_docs = list(collection.find(
            {'track_mbid': {'$in': unique_track_ids.tolist()}}
        ))
        existing_ab_df = pd.DataFrame(existing_ab_docs) if existing_ab_docs else pd.DataFrame()
        try:
            existing_track_ids = existing_ab_df['track_mbid'].to_list()
            print(f"Found {len(existing_track_ids)} tracks: {existing_track_ids}")
        except KeyError:
            existing_track_ids = []

        unseen_tracks_df = mb_df[~mb_df['track_mbid'].isin(existing_track_ids)]

        # Get new track data from AcousticBrainz API
        new_ab_df = unseen_tracks_df.apply(acousticbrainz_api.get_feature_data, axis=1)

        if not new_ab_df.empty:
            write_new_data(collection, new_ab_df)

        # Combine existing and new data
        dfs_to_concat = [df for df in [existing_ab_df, new_ab_df] if not df.empty]

        if not dfs_to_concat:
            return new_ab_df  # Return the all-NA new_ab_df (which is ok because it has the correct features)
        else:
            entire_ab_df = pd.concat(dfs_to_concat, ignore_index=True)
            print("entire_ab_df:", entire_ab_df)
            return entire_ab_df
    finally:
        client.close()


def write_new_data(collection, df_to_write):
    if df_to_write.empty:
        return

    # Drop NA values and convert to records
    df_clean = df_to_write.dropna()
    records = df_clean.to_dict('records')

    for record in records:
        try:
            collection.update_one(
                {'track_mbid': record['track_mbid']},
                {'$set': record},
                upsert=True
            )
        except DuplicateKeyError:
            print(f"Duplicate key found for track_mbid: {record['track_mbid']}")
