#!/usr/bin/python3
"""Create a view for state"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State

# Route to retrieve the list of all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])
