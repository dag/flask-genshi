# encoding=utf-8
from flask import Flask
from flaskext.genshi import Genshi, template_parsed
from genshi.core import TEXT
from genshi.filters import Transformer, Translator
from operator import methodcaller

from .blueprint import bp


app = Flask(__name__)
app.register_blueprint(bp)

genshi = Genshi(app)

translations = {
    u'Hello, %(name)s!': u'¡Hola, %(name)s!'
}


def gettext(string):
    return translations.get(string, string)


@genshi.filter('text/html')
def loud_paragraphs(stream):
    return stream | Transformer('//p').map(methodcaller('upper'), TEXT)


@template_parsed.connect_via(template_parsed.ANY)
def setup_translator(sender, template):
    Translator(gettext).setup(template)
