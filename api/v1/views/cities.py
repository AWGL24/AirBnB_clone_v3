#!/usr/bin/python3
"""new view for City objects that handles RESTFul API actions"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """retrives, delets and updates city objects"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(city_obj)
        storage.save()
        return ('{}', 200)

    if request.method == 'PUT':
        json_req = request.get_json()
        if json_req is None:
            return jsonify({'error': 'Not a JSON'}), 400

    for key, value in json.items():
        if key in ('id', 'state_id', 'updated_at', 'created_at'):
            continue
        setattr(city_obj, key, value)
        storage.save()
        return jsonify(city_obj.to_dict()), 200

    return jsonify(city_obj.to_dict())


@app_views.route('states/<state_id>/cities', methods=['GET'])
def get_city(state_id):
    """ the state based on the id """
    city_obj = storage.get('State', state_id)
    if city_obj is None:
        abort(404)
    cities = [city.to_dict() for city in city_obj.cities]
    return jsonify(cities), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create new city"""
    city_obj = storage.get('State', state_id)
    if city_obj is None:
        abort(404)
    json_req = request.get_json(silent=True)
    if json_req is None:
        abort(400, "Not a JSON")
    elif "name" not in json_req.keys():
        abort(400, "Missing Name")
    else:
        json_req['state_id'] = city_obj.id
        new = City(**json_req)
        storage.new(new)
        storage.save()
    return jsonify(new.to_dict()), 201
