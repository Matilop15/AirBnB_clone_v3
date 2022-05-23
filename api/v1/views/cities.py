#!/usr/bin/python3
"""Same as city, create a new view for
City objects that handles all default
RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models import state, storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_city(state_id):
    """
    Retrieves the list of all City objects of
    a State: GET /api/v1/states/<state_id>/cities
    """
    all_city = storage.all(city)
    list_city = []
    for city in all_city.values():
        list_city.append(city.to_dict())

    return jsonify(list_city)


@app_views.route('/city/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object: GET /api/v1/citys/<city_id>"""
    state = storage.get(State, state_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/city/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes a city object
    """
    city = storage.get(city, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/city', methods=['POST'], strict_slashes=False)
def post_city():
    """
    post a city object
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


@app_views.route('/city/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update a city object
    """
    city = storage.get(city, city_id)
    if city is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, value)
        storage.save()
        res = city.to_dict()
        return jsonify(res), 200
