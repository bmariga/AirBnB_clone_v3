#!/usr/bin/python3
"""Contains all REST actions for amenity Objects"""

# Import necessary modules and libraries
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

# Define a route to retrieve a list of all amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves amenity objects"""
    
    # Get all Amenity objects from storage
    amenity = storage.all(Amenity)
    
    # Create a list to store Amenity objects as dictionaries
    all_amenities = []
    
    # Iterate through each Amenity object, convert it to a dictionary, and append to the list
    for i in amenity.values():
        all_amenities.append(i.to_dict())
    
    # Return the list of Amenity objects as JSON
    return jsonify(all_amenities)

# Define a route to retrieve an amenity object by its ID
@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity_id(id):
    """retrieves an amenity object"""
    
    # Retrieve the Amenity object by its ID
    amenity = storage.get(Amenity, id)
    
    # If the Amenity doesn't exist, return a 404 error
    if amenity is None:
        abort(404)
    
    # Return the Amenity object as JSON
    return jsonify(amenity.to_dict())

# Define a route to delete an amenity object by its ID
@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    """deletes an amenity object"""
    
    # Retrieve the Amenity object by its ID
    amenity = storage.get(Amenity, id)
    
    # If the Amenity doesn't exist, return a 404 error
    if amenity is None:
        abort(404)
    
    # Delete the Amenity object, save the changes, and return an empty dictionary with a status code 200
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

# Define a route to create a new amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates an amenity object"""
    
    # Check if the request data is not in JSON format
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    # Check if the 'name' key is missing in the JSON data
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    
    # Get the JSON data from the request
    data = request.get_json()
    
    # Create a new Amenity object using the JSON data
    amenity = Amenity(**data)
    
    # If the Amenity is not created successfully, return a 404 error
    if amenity is None:
        abort(404)
    
    # Return the newly created Amenity object as JSON with a status code 201
    return jsonify(amenity.to_dict()), 201

# Define a route to update an amenity object by its ID
@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    """updates an amenity object"""
    
    # Retrieve the Amenity object by its ID
    amenity = storage.get(Amenity, id)
    
    # If the Amenity doesn't exist, return a 404 error
    if amenity is None:
        abort(404)
    
    # Check if the request data is not in JSON format
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    # List of keys to ignore when updating the Amenity object
    ignore_keys = ['id', 'created_at', 'updated_at']
    
    # Check if the 'name' key is in the JSON data, and if so, update the Amenity's name
    if 'name' in request.get_json():
        amenity.name = request.get_json()['name']
    
    # Save the updated Amenity object and return it as JSON with a status code 200
    amenity.save()
    return jsonify(amenity.to_dict()), 200

