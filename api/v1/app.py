#!/user/bin/python3
"""
Create the API
"""
from os import getenv
from flask import Flask, Blueprint
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """Closes storage session"""
    storage.close()

if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(debug=True, host=api_host, port=int(api_port), threaded=True)
