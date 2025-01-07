from flask import request, session, jsonify
import os
from . import app
from .match import get_matches, spider_plot
from .show_responses import get_dj_show_info
from pymongo import MongoClient
from dotenv import load_dotenv


# Initialize MongoDB connection at startup
load_dotenv()
client = MongoClient(os.getenv('MONGO_CONNECTION_URI'))
artists_collection = client['artists']['artist_names_and_mbids']

# Create a text index on the name field
artists_collection.create_index([('name', 'text')])


@app.route('/api/mood', methods=['POST'])
def receive_mood():
    # TODO allow the user to select multiple moods

    session.pop('mood', None)
    data = request.get_json()
    mood = data['mood']
    if not mood:
        return jsonify({'error': 'No mood'}), 400

    session['mood'] = mood
    print('in receive_mood:', session['mood'])

    return jsonify({'message': 'Mood received successfully'}), 200


@app.route('/api/artists', methods=['POST'])
def receive_artists():
    session.pop('artists_data', None)
    data = request.get_json()
    print(data)
    artists_data = data['artists_data']
    if not artists_data:
        return jsonify({'error': 'No artists'}), 400

    session['artists_data'] = artists_data
    print('in receive_artists:', session['artists_data'], session['mood'])

    return jsonify({'message': 'Artists received successfully'}), 200


@app.route('/api/results', methods=['GET', 'POST'])
def results():
    top_djs, dj_features, user_features = get_matches(session.get('mood', 'happy'), session.get('artists_data', None), [])

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

    # Data for the DJ match from the show responses Excel file (e.g. About Me, timeslot, show name, etc.)
    match_show_info = get_dj_show_info(match_id)
    results.update(match_show_info)


    # TODO add "Is this a good recommendation?" Thumbs up or thumbs down pop-up

    return jsonify({'results': results}), 200


@app.route('/api/search/artists', methods=['GET'])
def search_artists():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required.'}), 400

    artists_data = list(artists_collection.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([
        ("score", {"$meta": "textScore"})
    ]).limit(3))

    # Clean up the ObjectId for JSON serialization
    for artist in artists_data:
        artist['_id'] = str(artist['_id'])
    print(artists_data)

    return jsonify({'artists_data': artists_data}), 200
