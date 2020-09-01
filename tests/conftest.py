import pytest
from .flask_genshi_testapp import create_app


@pytest.fixture
def app(request):
    return create_app()


@pytest.fixture
def context():
    return dict(name="Rudolf")
