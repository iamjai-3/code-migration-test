from flask import request, jsonify
from data.storage import data

def handle():
    input_data = request.get_json()
    id = len(data) + 1
    data[id] = {
        'id': id,
        'name': input_data['name'],
        'description': input_data['description']
    }
    return jsonify(data[id])