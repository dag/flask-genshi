from flask import Flask
from flask_genshi import Genshi

from .test_blueprint import test_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(test_blueprint)
    Genshi(app)
    return app
