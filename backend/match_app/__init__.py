from flask import Flask
from .config import FLASK_SECRET_KEY

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Import routes.py, which handles the core logic
from . import routes
