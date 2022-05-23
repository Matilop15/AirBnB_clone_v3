#!/usr/bin/python3
"""Create a new view for Places
objects that handles all default RESTFul API actions
"""
from api.v1.views.states import all_states
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Places objects
    of a specific city
    """
    list_cities = []
    city = storage.get(City, city_id)
    if not state:
        abort(404)
    for citys in city.cities:
        list_cities.append(citys.to_dict())

    return jsonify(list_cities)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(places_id):
    """Retrieves a Paces object. : GET /api/v1/places/<place_id>"""
    placess = storage.get(Place, place_id)
    if placess:
        return jsonify(placess.to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Places object: DELETE /api/v1/places/place_id'
    """
    placess = storage.get(Place, place_id)
    if placess is None:
        abort(404)
    else:
        storage.delete(placess)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    """
    cityy = storage.get(City, city_id)
    if not cityy:
        abort(404)

    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    elif 'user_id' not in post.keys():
        abort(400, "Missing name")
    elif 'name' not in post.keys():
        abort(400, "Missing name")
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        instance = Place(**post)
        storage.new(instance)
        storage.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object: PUT /api/v1/places/<place_id>
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(places, key, value)
        storage.save()
        res = places.to_dict()
        return jsonify(res), 200