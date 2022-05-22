#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions
"""
from models.state import State
from models import storage
from os import abort
from flask import Flask, jsonify

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
        return jsonify(list_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save
    
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
