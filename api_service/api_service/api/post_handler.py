from flask import request, jsonify
from data.store import data

def handle_post():
    input_data = request.get_json()
    new_id = len(data) + 1
    data[new_id] = {
        'id': new_id,
        'name': input_data['name'],
        'description': input_data['description']
    }
    return jsonify(data[new_id])