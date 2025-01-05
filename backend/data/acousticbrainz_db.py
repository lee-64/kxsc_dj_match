import pandas as pd
import sqlite3 as sl
from api_helpers import acousticbrainz_api


def setup_db(connection, cursor):
    """Ensure the database and table are set up."""

    # TODO add "Song name" and "artist_mbid" columns to search based off of song names within an artist id, since some songs have multiple mbids (eg Radiohead)
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS AcousticBrainz (
            track_mbid TEXT PRIMARY KEY,
            key TEXT,
            key_scale TEXT,
            key_confidence REAL,
            danceability REAL,
            bpm INTEGER,
            instrumental INTEGER,
            instrumental_confidence REAL,
            gender INTEGER,
            gender_confidence REAL,
            danceable INTEGER,
            danceable_confidence REAL,
            tonal INTEGER,
            tonal_confidence REAL,
            timbre INTEGER,
            timbre_confidence REAL,
            electronic INTEGER,
            electronic_confidence REAL,
            party INTEGER,
            party_confidence REAL,
            aggressive INTEGER,
            aggressive_confidence REAL,
            acoustic INTEGER,
            acoustic_confidence REAL,
            happy INTEGER,
            happy_confidence REAL,
            sad INTEGER,
            sad_confidence REAL,
            relaxed INTEGER,
            relaxed_confidence REAL,   
            gztan_model TEXT,
            gztan_genre_confidence REAL,
            electronic_classification TEXT,
            electronic_genre_confidence REAL,            
            dortmund TEXT,
            dortmund_genre_confidence REAL,            
            rosamerica TEXT,
            rosamerica_confidence REAL
            )
        """)
        connection.commit()

    except Exception as e:
        print(e)



def get_db_connection():
    """Return a new SQLite connection."""
    db_path = "data/acousticbrainz_data.db"
    return sl.connect(db_path)





def modify_ab_db(mb_df):

    with get_db_connection() as conn:
        cursor = conn.cursor()

        setup_db(conn, cursor)


        unique_track_ids = mb_df['track_mbid'].unique()

        existing_ab_df = get_existing_data(cursor, unique_track_ids)
        print("existing_ab_df:", existing_ab_df)
        try:
            existing_track_ids = existing_ab_df['track_mbid'].to_list()
        except KeyError:
            existing_track_ids = []
        print("existing_track_ids:", existing_track_ids)

        unseen_tracks_df = mb_df[~mb_df['track_mbid'].isin(existing_track_ids)]
        print("unseen_tracks_df:", unseen_tracks_df)

        new_ab_df = unseen_tracks_df.apply(acousticbrainz_api.get_feature_data, axis=1)

        print("new_ab_df:", new_ab_df)

        write_new_data(conn, cursor, new_ab_df)

        conn.commit()

        # Filter non-empty DataFrames before concatenation
        dfs_to_concat = [df for df in [existing_ab_df, new_ab_df] if not df.empty]

        if not dfs_to_concat:
            return new_ab_df  # Return the all-NA new_ab_df (which is ok because it has the correct features)
        else:
            entire_ab_df = pd.concat(dfs_to_concat, ignore_index=True)
            print("entire_ab_df:", entire_ab_df)
            return entire_ab_df



def get_existing_data(cursor, ids):
    query = f"SELECT * FROM AcousticBrainz WHERE track_mbid IN ({','.join(['?'] * len(ids))})"
    cursor.execute(query, ids)
    data = cursor.fetchall()

    # Extract column names from the cursor description
    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=columns)
    return df


def write_new_data(connection, cursor, df):
    query = """
    INSERT OR REPLACE INTO AcousticBrainz (
        track_mbid,
        key,
        key_scale,
        key_confidence,
        danceability,
        bpm,
        instrumental,
        instrumental_confidence,
        gender,
        gender_confidence,
        danceable,
        danceable_confidence,
        tonal,
        tonal_confidence,
        timbre,
        timbre_confidence,
        electronic,
        electronic_confidence,
        party,
        party_confidence,
        aggressive,
        aggressive_confidence,
        acoustic,
        acoustic_confidence,
        happy,
        happy_confidence,
        sad,
        sad_confidence,
        relaxed,
        relaxed_confidence,
        gztan_model,
        gztan_genre_confidence,
        electronic_classification,
        electronic_genre_confidence,
        dortmund,
        dortmund_genre_confidence,
        rosamerica,
        rosamerica_confidence
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """

    df.dropna(inplace=True)  # Don't write any NA values to the database

    # Convert DataFrame to native Python types before inserting
    values = [tuple(x.astype(object)) for x in df.to_numpy()]
    print("values:", values)
    print("*"*40)
    print("values to add:", values)
    print("*"*40)

    cursor.executemany(query, values)
    connection.commit()


if __name__ == "__main__":
    with get_db_connection() as conn:
        cursor = conn.cursor()

        setup_db(conn, cursor)
