#!/usr/bin/python3
"""Same as State, create a new view for City
objects that handles all default RESTFul API actions
"""
from api.v1.views.states import all_states
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object. : GET /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object: DELETE /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    Creates a City: POST /api/v1/states/<state_id>/cities
    """
    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    elif 'name' not in post.keys():
        abort(400, "Missing name")
    else:
        instance = City(**post)
        storage.new(instance)
        storage.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_citie(city_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, value)
        storage.save()
        res = city.to_dict()
        return jsonify(res), 200
