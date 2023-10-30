#!/usr/bin/python3
'''
RESTful API for class User
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    return all user objects in json form
    '''
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())

    return jsonify(user_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_userId(user_id):
    '''return user with id'''
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''delete user'''
    user = storage.get('user', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()

    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''create user'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        json_data = request.get_json()
        obj = User(**json_data)
        obj.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''update user'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    json_data = request.get_json()
    ignore_keys  = ("id", "email", "created_at", "updated_at")
    for key, value in json_data.items():
        if key not in ignore_keys:
            user.__dict__[key] = value

    user.save()
    return jsonify(user.to_dict()), 200
