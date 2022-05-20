#!/usr/bin/python3
""" module holds app """
from flask import Flask
from models import storage
from api.v1.views import views

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/')
    def create_app():

    @app.teardown_appcontext
