#!/usr/bin/python3
""" Module containing views """
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """status api"""
    return jsonify({"status": "OK"})
