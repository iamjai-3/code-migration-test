from flask import request, jsonify
from data.storage import data

def handle():
    id = request.args.get('id')
    
    if not id:
        return jsonify({'message': 'ID is required'}), 400
        
    id = int(id)
    if id not in data:
        return jsonify({'message': 'Item not found'}), 404
        
    del data[id]
    return jsonify({'message': 'Item deleted'})