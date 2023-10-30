#!/usr/bin/python3
"""Contains all REST actions for amenity Objects"""

# Import necessary modules and libraries
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


# Define a route to retrieve a list of all amenity objects
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """retrieves review objects"""
    # Get all Amenity objects from storage
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for obj in place.reviews:
        reviews.append(obj.to_dict())

    # return reviews
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''review deletion'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    # delete review
    storage.delete(review)
    storage.save()

    # return empty
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    '''return review by id'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    # return dic of review
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review():
    '''create review'''
    if not request.get_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif storage.get(Place, place_id) is None:
        abort(404)
    elif storage.get(User, request.get_json()["user_id"]) is None:
        abort(404)
    elif "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    else:
        json_data = request.get_json()
        obj = Review(**json_data)
        obj.place_id = place_id
        obj.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''update review'''
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    elif not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        json_data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        for key, value in json_data.items():
            if key not in ignore_keys:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
