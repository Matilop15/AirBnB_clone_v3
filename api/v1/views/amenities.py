#!/usr/bin/python3
"""Create a new view for Amenity
objects that handles all default RESTFul API actions
"""
from api.v1.views.states import all_states
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenities objects"""
    list_amenities = []
    amen = storage.all(Amenities)
    if not amen:
        abort(404)
    for ameniti in amen.values():
        list_amenities.append(ameniti.to_dict())

    return jsonify(list_amenities)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a City object. : GET /api/v1/cities/<city_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a City object: DELETE /api/v1/cities/<city_id>
    """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    else:
        storage.delete(amen)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """
    Creates a City: POST /api/v1/states/<state_id>/cities
    """
    amen = storage.get(Amenity)
    if not amen:
        abort(404)

    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    elif 'name' not in post.keys():
        abort(400, "Missing name")
    else:
        instance = Amenity(**post)
        instance.amenity_id = amenity_id
        instance.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenitie(amenity_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amen, key, value)
        storage.save()
        res = amen.to_dict()
        return jsonify(res), 200
