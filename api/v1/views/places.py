#!/usr/bin/python3
"""Contains all REST actions for place Objects"""

# Import necessary modules
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models import storage
from models.city import City

# Define a route to retrieve a list of all Place objects of a city
@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves a list of all Place objects of a city"""
    city = storage.get(City, city_id)
    
    # If the city is not found, return a 404 error
    if city is None:
        abort(404)
    
    # Get the list of places from the city and return them as JSON
    places = city.places
    return jsonify([val.to_dict() for val in places])

# Define a route to retrieve a Place object by its ID
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    
    # If the place is not found, return a 404 error
    if place is None:
        abort(404)
    
    # Return the Place object as JSON
    return jsonify(place.to_dict())

# Define a route to delete a Place object by its ID
@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    
    # If the place is not found, return a 404 error
    if place is None:
        abort(404)
    
    # Delete the place, save the changes, and return an empty JSON response
    storage.delete(place)
    storage.save()
    return jsonify({})

# Define a route to create a new Place object
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def update_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    
    # If the city is not found, return a 404 error
    if city is None:
        abort(404)
    
    # Check if the request data is in JSON format
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    # Check if 'user_id' and 'name' are present in the request JSON
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    
    # Get the user based on 'user_id'
    user = storage.get(User, request.json['user_id'])
    
    # If the user is not found, return a 404 error
    if user is None:
        abort(404)
    
    # Create a new Place object, save it, and return it as JSON
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)

