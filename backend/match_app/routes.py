from flask import request, session, jsonify
from . import app
from .match import get_matches, spider_plot
from .show_responses import get_dj_show_info
from .database_connection import get_db
from dotenv import load_dotenv
import re

load_dotenv()


@app.route('/api/mood', methods=['POST'])
def receive_mood():
    """
    Stores user's mood selection in session.
    Expects JSON payload with 'mood' field.

    :return: JSON response with success message or error, status code
    """

    session.pop('mood', None)  # Clear old mood
    data = request.get_json()
    mood = data['mood']

    if not mood:
        return jsonify({'error': 'No mood'}), 400

    session['mood'] = mood  # Store the user's mood in session
    return jsonify({'message': 'Mood received successfully'}), 200


@app.route('/api/artists', methods=['POST'])
def receive_artists():
    """
    Stores user's selected artists in session.
    Expects JSON payload with 'artists_data' field.

    :return: JSON response with success message or error, status code
    """

    session.pop('artists_data', None)  # Clear old artists
    data = request.get_json()
    artists_data = data['artists_data']

    if not artists_data:
        return jsonify({'error': 'No artists'}), 400

    session['artists_data'] = artists_data  # Store the user's artists in session
    return jsonify({'message': 'Artists received successfully'}), 200


@app.route('/api/results', methods=['GET', 'POST'])
def results():
    """
    Fetches DJ recommendations based on user's mood and artists.

    :return: JSON with DJ matches, percentages, spider plot, and show info, status code
    """

    user_mood = session.get('mood', 'happy')
    user_artists = session.get('artists_data', None)
    top_djs, dj_features, user_features = get_matches(user_mood, user_artists)  # Fetch match data from match.py

    # Parse the match data
    match_name = top_djs[0]['dj_name']
    match_id = top_djs[0]['dj_id']
    top_dj_names = [dj['dj_name'] for dj in top_djs]
    top_dj_percentages = [dj['match_percent'] for dj in top_djs]
    fig = spider_plot(user_features, dj_features, match_name)

    results = ({
        'dj_match': match_name,
        'top_djs': top_dj_names,
        'match_percentages': top_dj_percentages,
        'spider_fig': fig
    })

    # Append the DJ match's show responses data (e.g. About Me, timeslot, show name, etc.)
    match_show_info = get_dj_show_info(match_id)
    results.update(match_show_info)

    return jsonify({'results': results}), 200


@app.route('/api/search/artists', methods=['GET'])
def search_artists():
    """
    Searches artists collection in MongoDB using a combination of query regex matching and (approximate) popularity to
    find the most relevant artists (up to 3).

    :return: JSON with the first 3 artists' data (MongoDB _id, artist name, artist MusicBrainz ID), sorted by relevance
    """

    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required.'}), 400

    # Get fresh connection for each request
    client = get_db()
    artists_collection = client['artists']['artist_names_and_mbids']

    regex_pattern = f"^{re.escape(query)}"
    try:
        # artists_collection.create_index([('name', 'text')])  # Create a text index on name field if it doesn't exist
        # Search for regex matches and sort the results by popularity
        artists_data = list(artists_collection.find(
            {"name": {"$regex": regex_pattern, "$options": "i"}},  # Case-insensitive
            {"name": 1, "mbid": 1}
        ).sort([("_id", 1)]).limit(3))  # _id acts as a proxy for popularity because documents are in descending popularity (approximately) order

        # Clean up the ObjectId for JSON serialization
        for artist in artists_data:
            artist['_id'] = str(artist['_id'])

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        client.close()

    return jsonify({'artists_data': artists_data}), 200
