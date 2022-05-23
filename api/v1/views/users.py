#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects: GET /api/v1/users"""
    all_users = storage.all(User)
    list_users = []
    for user in all_users.values():
        list_users.append(user.to_dict())

    return jsonify(list_users)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object: GET /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object:: DELETE /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User: POST /api/v1/users
    """
    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    elif 'email' not in post.keys():
        abort(400, "Missing email")
    elif 'password' not in post.keys():
        abort(400, "Missing password")
    else:
        instance = User(**post)
        storage.new(instance)
        storage.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object: PUT /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                pass
            else:
                setattr(user, key, value)
        storage.save()
        res = user.to_dict()
        return jsonify(res), 200
