#!/usr/bin/python3
"""
I don´tknow
"""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
	"""Return ok"""
	return {'status': 'OK'}
