#!/usr/bin/python3
"""
Created a view for City objects that handels RESTful API
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves the list of user objects """
    user_list = []
    for user in user_list.storage.all('User').items():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def usersids(user_id):
    """ Retrieves user object by id """
    userid = storage.get(User, user_id)
    if userid is None:
        abort(404)
    return jsonify(userid.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def users_delete(user_id):
    """ Deletes a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    """ creates a new user """
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if 'email' not in json_req:
        abort(400, 'Missing email')
    if 'password' not in json_req:
        abort(400, 'Missing password')
    new_user = User(**json_req)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_update(user_id):
    """ Updates a user object by id """
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in json_req.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
