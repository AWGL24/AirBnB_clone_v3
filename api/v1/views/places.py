#!/usr/bin/python3
"""
Module handels new view for place objects that handles RESTFul API actions
"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves list of all place objects of a city"""
    city_obj = storage.get(City, city_id)
    plist = []
    if city_obj is None:
        abort(404)
    for place in city_obj.places:
        plist.append(place.to_dict())
    return jsonify(plist)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_id(place_id):
    """ Retrieves a places object by id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<places_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place based on id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create place"""
    if storage.get(City, city_id) is None:
        abort(404)
    json_req = request.get_json(silent=True)
    if json_req is None:
        abort(400, "Not a JSON")
    if "user_id" not in json_req:
        abort(400, "Missing user_id")
    user_obj = storage.get('User', json_req["user_id"])
    if user_obj is None:
        abort(404)
    if "name" not in json_req:
        abort(400, "Missing name")
    json_req["city_id"] = city_id
    new = Place(**json_req)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    json_req = request.get_json(silent=True)
    if json_req is None:
        abort(400, "Not a JSON")
    for key, value in json_req.items():
        if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            pass
        else:
            setattr(place_obj, key, value)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
