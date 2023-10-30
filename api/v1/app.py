#!/usr/bin/python3
"""creating a flask application"""

# Import necessary libraries and modules
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# CORS instance allowing: /* for 0.0.0.0
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# Register the blueprint app_views
app.register_blueprint(app_views)

# Declare a method to handle teardown
@app.teardown_appcontext
def teardown(exception):
    """closes the current SQLAlchemy session"""
    storage.close()

# Define a JSON error handler for 404 Not Found errors
@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 Not found errors"""
    return ({'error': 'Not found'}, 404)

# Check if this script is the main entry point
if __name__ == '__main__':
    # Retrieve the host and port settings from environment variables
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # Note: getenv returns a string, and port is converted to an integer
    # THREADED is set to true so it can serve multiple requests at once
    app.run(host=host, port=port, threaded=True)

