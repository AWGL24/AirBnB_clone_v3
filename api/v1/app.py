#!/usr/bin/python3
""" module holds app """
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def tear(exception):
    """ tear method """
    storage.close()


if __name__ == "__main__":
    setup_global_errors()
    app.run(host=host, port=port)
