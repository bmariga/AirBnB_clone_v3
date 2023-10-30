#!/usr/bin/python3
'''
Creating a new view for Amenity objects
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    '''return amenities object'''
    amenity_list = []
    for i in storage.all('Amenity').values():
        amenity_list.append(i.to_dict())
    
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_id(amenity_id):
    '''get amenity by id'''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''delete amenity'''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    '''create amenity'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_json = request.get_json()
        obj = Amenity(**obj_json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenities_id>',methods=['PUT'])
def update_amenity(amenities_id):
    '''updat amenity'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get("Amenity", amenities_id)
    if amenity is None:
        abort(404)
    obj_json = request.get_json()
    ignore_keys  = ("id", "created_at", "updated_at")
    for key, value in obj_json.items():
        if key not in ignore_keys:
            amenity.__dict__[key] = value
    amenity.save()
    return jsonify(amenity.to_dict()), 200
