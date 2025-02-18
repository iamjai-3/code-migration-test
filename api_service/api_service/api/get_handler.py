from flask import request, jsonify
from data.store import data

def handle_get():
    item_id = request.args.get('id')
    if item_id:
        item_id = int(item_id)
        if item_id in data:
            return jsonify(data[item_id])
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(list(data.values()))