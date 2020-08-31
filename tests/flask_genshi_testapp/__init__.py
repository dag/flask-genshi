from flask import Flask
from flaskext.genshi import Genshi


def create_app():
    app = Flask(__name__)
    genshi = Genshi(app)
    return app
