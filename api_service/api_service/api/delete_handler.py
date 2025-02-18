from flask import request, jsonify
from data.store import data

def handle_delete():
    item_id = request.args.get('id')
    
    if not item_id:
        return jsonify({'message': 'ID is required'}), 400
        
    item_id = int(item_id)
    if item_id not in data:
        return jsonify({'message': 'Item not found'}), 404
        
    del data[item_id]
    return jsonify({'message': 'Item deleted'})