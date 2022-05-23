#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
        return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonifi({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    post a State object
    """
    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    elif 'name' not in post.keys():
        abort(400, "Missing name")
    else:
        instance = State(**post)
        storage.new(instance)
        storage.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    update a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
        storage.save()
        res = state.to_dict()
        return jsonify(res), 200
