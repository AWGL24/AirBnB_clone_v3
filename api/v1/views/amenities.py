#!/usr/bin/python3
"""new view for State objects that handles RESTFul API actions"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views, index


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """list amenities objects"""
    amenity_obj = []
    for obj in storage.all('Amenity').values():
        amenity_obj.append(obj.to_dict())
    return jsonify(amenity_obj)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Retrieves a amenity object by id """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities_id(amenity_id):
    """ Deletes a amenity based on id """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        storage.delete(amenity_obj)
        storage.save()
    return jsonify(({}), 200)


@ app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create amenity"""
    json_req = request.get_json(silent=True)
    if json_req is None:
        abort(400, "Not a JSON")
    elif "name" not in json_req.keys():
        abort(400, "Missing Name")
    else:
        new = Amenity(**json_req)
        storage.new(new)
        storage.save()
    return jsonify(new.to_dict(()), 201)


@ app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                  strict_slashes=False)
def update_amenities(amenity_id):
    """ Updates amenity object """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)

    json_req = request.get_json(silent=True)
    if json_req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in json_req.values():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenity_obj, key, value)
        storage.save()
        return jsonify(amenity_obj.to_dict()), 200
