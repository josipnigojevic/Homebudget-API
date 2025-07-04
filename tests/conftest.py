import os, sys
import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from homebudget import create_app, db
from homebudget.models.user import User
from homebudget.models.category import Category

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "doktorpavlovicbokkiropraktike"
    })
    with app.app_context():
        db.create_all()
    return app

@pytest.fixture
def auth_header(app):
    with app.app_context():
        user = User(username="testuser", starting_budget=0)
        user.set_password("testpass")
        for name in ["Food","Car","Accommodation","Gifts","Health","Utilities"]:
            user.categories.append(Category(name=name))
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client(app, auth_header):
    class AuthClient(FlaskClient):
        def open(self, *args, **kwargs):
            if "headers" in kwargs:
                headers = kwargs["headers"]
                headers.update(auth_header)
                kwargs["headers"] = headers
            return super().open(*args, **kwargs)

    app.test_client_class = AuthClient
    return app.test_client()

@pytest.fixture
def category_id(client):
    res = client.get("/categories")
    return res.get_json()[0]["id"]
