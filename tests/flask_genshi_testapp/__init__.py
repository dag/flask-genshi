
from flask import Flask
from extensions import genshi

import package_mod as pkgmod
import views.module_mod as modmod


app = Flask(__name__)
app.register_module(pkgmod.mod)
app.register_module(modmod.mod)

genshi.init_app(app)
