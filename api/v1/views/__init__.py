#!/usr/bin/python3
""" Init defintion for views package"""

# Import the Blueprint class from Flask
from flask import Blueprint

# Create a Flask Blueprint named "app_views" with a URL prefix of "/api/v1"
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# import of everything in the package api.v1.views.index
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
