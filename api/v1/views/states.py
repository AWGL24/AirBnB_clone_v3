#!/usr/bin/python3
"""new view for State objects that handles RESTFul API actions"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """list state objects"""
    state_obj = []
    for obj in storage.all('State').items():
        state_obj.append(obj.to_dict())
    return jsonify(state_obj)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_stateid(state_id):
    """ Retrieves a state object by id """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state based on id """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    state_obj.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """create state"""
    json_req = request.get_json()
    if json_req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in json_req:
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**json_req)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a state object """
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    for key, value in json_req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
