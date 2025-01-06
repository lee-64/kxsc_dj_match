from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = secret_key

# Import routes.py, which handles the core logic
from . import routes
