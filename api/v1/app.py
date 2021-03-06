#!/usr/bin/python3
"""
 folder api at the root of the project
 with an empty file __init__.py
"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from api.v1.views.index import *
from models import storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler 404 error"""
    return jsonify({'error': "Not found"}), 404


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(debug=True, host=api_host, port=int(api_port), threaded=True)
