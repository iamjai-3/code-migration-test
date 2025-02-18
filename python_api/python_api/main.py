from flask import Flask, request, jsonify
from api import get, post, put, delete

app = Flask(__name__)


@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def handle_request():
    if request.method == "GET":
        return get.handle()
    elif request.method == "POST":
        return post.handle()
    elif request.method == "PUT":
        return put.handle()
    elif request.method == "DELETE":
        return delete.handle()
    else:
        return jsonify({"message": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True)
