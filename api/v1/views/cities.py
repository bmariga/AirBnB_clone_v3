#!/usr/bin/python3
"""Contains all REST actions for city Objects"""

# Import necessary modules and libraries
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.city import City
from models import storage
from models.state import State

# Define a route to retrieve a list of all city objects of a State
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieves a list of all city objects of State"""
    # Retrieve the State object by its ID
    state = storage.get(State, state_id)
    
    # If the State doesn't exist, return a 404 error
    if state is None:
        abort(404)
    
    # Get the list of cities associated with the State and return them as JSON
    cities = state.cities
    return jsonify([val.to_dict() for val in cities])

# Define a route to retrieve a city object by its ID
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """retrieves a city object"""
    # Retrieve the City object by its ID
    city = storage.get(City, city_id)
    
    # If the City doesn't exist, return a 404 error
    if city is None:
        abort(404)
    
    # Return the City object as JSON
    return jsonify(city.to_dict())

# Define a route to delete a city object by its ID
@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city object"""
    # Retrieve the City object by its ID
    city = storage.get(City, city_id)
    
    # If the City doesn't exist, return a 404 error
    if city is None:
        abort(404)
    
    # Delete the City object, save the changes, and return an empty dictionary
    storage.delete(city)
    storage.save()
    return jsonify({})

# Define a route to create a new city object
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city object"""
    # Retrieve the State object by its ID
    state = storage.get(State, state_id)
    
    # If the State doesn't exist, return a 404 error
    if state is None:
        abort(404)
    
    # Check if the request data is not in JSON format
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    # Check if the 'name' key is missing in the JSON data
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    
    # Create a new City object and save it
    city = City(name=request.get_json()['name'], state_id=state_id)
    city.save()
    
    # Return the newly created City object as JSON with a status code 201
    return make_response(jsonify(city.to_dict()), 201)

# Define a route to update a city object by its ID
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city object"""
    # Retrieve the City object by its ID
    city = storage.get(City, city_id)
    
    # If the City doesn't exist, return a 404 error
    if city is None:
        abort(404)
    
    # Check if the request data is not in JSON format
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    # Check if the 'name' key is in the JSON data, and if so, update the City's name
    if 'name' in request.json:
        city.name = request.get_json()['name']
        city.save()
    
    # Return the updated City object as JSON
    return jsonify(city.to_dict())

