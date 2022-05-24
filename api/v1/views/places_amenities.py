#!/usr/bin/python3
"""Create a new view for the link between Place
objects and Amenity objects that handles all
default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
import os


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id=None):
    """
    Retrieves the list of all Amenity objects of a Place:
    GET /api/v1/places/<place_id>/amenities
    """
    if place_id is None:
        abort(404)
    list_places_amenities = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        obj_amenities = place.amenities
    else:
        obj_amenities = place.amenity_ids
    for amenity in obj_amenities:
        list_places_amenities.append(amenity.to_dict())

    return jsonify(list_places_amenities)


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

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
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

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amanity_ids
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
