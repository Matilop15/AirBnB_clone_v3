#!/usr/bin/python3
"""Create a new view for the link between Place
objects and Amenity objects that handles all
default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import amenities, app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from os import environ


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id=False):
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
    if environ.get('HBNB_TYPE_STORAGE') != "db":
        amens = storage.all(Amenity)
        for amenity in amens.values():
            if amenity.id in place.amenity_ids:
                list_places_amenities.append(amenity)
    else:
        list_places_amenities = place.amenities

    return jsonify([amenity.to_dict() for amenity in list_places_amenities])


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

    if environ.get('HBNB_TYPE_STORAGE') != "db":
        if amenity not in place.amenities:
            abort(404)
        index = None
        for idx, id in enumerate(place.amenity_ids):
            if amenity.id == id:
                index = idx
                break
        del place.amenity_ids[index]
        place.save()      
    else:
        index = None
        for idx, amen in enumerate(place.amenities):
            if amen_id == amenity_ids:
               index = idx
               break
            if index is None:
               abort(404)
        del place.amenities[index]
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

    if environ.get('HBNB_TYPE_STORAGE') != "db":
        if amenity in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
            place.save()
            return jsonify(amenity.to_dict()), 201
    else:
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
