from flask import request, jsonify
from data.storage import data

def handle():
    input_data = request.get_json()
    id = request.args.get('id')
    
    if not id:
        return jsonify({'message': 'ID is required'}), 400
        
    id = int(id)
    if id not in data:
        return jsonify({'message': 'Item not found'}), 404
        
    data[id]['name'] = input_data.get('name', data[id]['name'])
    data[id]['description'] = input_data.get('description', data[id]['description'])
    
    return jsonify(data[id])