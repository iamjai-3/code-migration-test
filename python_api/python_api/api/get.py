from flask import request, jsonify
from data.storage import data

def handle():
    id = request.args.get('id')
    if id:
        id = int(id)
        if id in data:
            return jsonify(data[id])
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(list(data.values()))