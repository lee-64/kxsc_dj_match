import json
import os


def load_app_config():
    # Get absolute path of the current file being run.
    # Makes the config path correct no matter the project's location, user's operating system, etc.
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(cur_dir)
    config_path = os.path.join(parent_dir, 'config', 'config.json')

    with open(config_path) as config_file:
        return json.load(config_file)


config = load_app_config()

FLASK_SECRET_KEY = config['flask']['secret_key']
