from flask import Flask
from flask_genshi import Genshi


def create_app():
    app = Flask(__name__)
    genshi = Genshi(app)
    return app
