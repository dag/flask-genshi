
from flask import Flask
from flaskext.genshi import Genshi

import package_mod as pkgmod
import views.module_mod as modmod


def create_app():
    app = Flask(__name__)
    app.register_module(pkgmod.mod)
    app.register_module(modmod.mod)

    genshi = Genshi(app)

    return app
