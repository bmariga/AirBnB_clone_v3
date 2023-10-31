#!/usr/bin/python3
"""Returns a JSON response"""

# Import the 'jsonify' function from Flask and necessary modules
from flask import jsonify
from api.v1.views import app_views
from models import storage

# Route for the '/status' endpoint
@app_views.route('/status')
def status_check():
    '''Returns status code'''
    # Return a JSON response with the status "OK"
    return jsonify({"status": "OK"})


# Route for the '/stats' endpoint
@app_views.route('/stats', methods=['GET'])
def object_stats():
    """Retrieves the number of each object by type"""
    
    # Use the 'storage.count()' method to fetch the count of each object type
    objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User'),
    }
    
    # Return a JSON response with the counts for each object type
    return jsonify(objects)

