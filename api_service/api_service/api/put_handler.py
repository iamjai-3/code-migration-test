from flask import request, jsonify
from data.store import data

def handle_put():
    input_data = request.get_json()
    item_id = request.args.get('id')
    
    if not item_id:
        return jsonify({'message': 'ID is required'}), 400
        
    item_id = int(item_id)
    if item_id not in data:
        return jsonify({'message': 'Item not found'}), 404
        
    data[item_id]['name'] = input_data.get('name', data[item_id]['name'])
    data[item_id]['description'] = input_data.get('description', data[item_id]['description'])
    
    return jsonify(data[item_id])