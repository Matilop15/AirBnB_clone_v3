#!/usr/bin/python3
"""Create a new view for the link between Place
objects and Amenity objects that handles all
default RESTFul API actions
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import *


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id=None):
    """
    Retrieves the list of all Amenity objects of a Place:
    GET /api/v1/places/<place_id>/amenities
    """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in getattr(place, "amenities")])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place:
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place:
    POST /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
