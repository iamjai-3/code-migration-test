from flask import Flask, request, jsonify
from api.get_handler import handle_get
from api.post_handler import handle_post
from api.put_handler import handle_put
from api.delete_handler import handle_delete

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_request():
    if request.method == 'GET':
        return handle_get()
    elif request.method == 'POST':
        return handle_post()
    elif request.method == 'PUT':
        return handle_put()
    elif request.method == 'DELETE':
        return handle_delete()
    else:
        return jsonify({'message': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)