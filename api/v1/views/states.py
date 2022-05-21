#!/user/bin/python3
"""new view for State objects that handles RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_state():
    """list state objects"""
    state_obj = []
    for obj in storage.all('State').values():
        state_obj.append(obj.to_dict())
    return jsonify(state_obj)


@app_views.route('/states', methods=['POST'])
def post_state():
    """create state"""
    json_req = request.get_json()
    if json_req is None:
        return jsonify({'error': 'Missing name'}), 400
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**json_req)
    storage.new(new_state)
    storage.save()
    return jsonify({'id': new_state.id, 'name': new_state.name}), 201
