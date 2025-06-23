import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_login_fail(client):
    response = client.post("/login", json={"username": "x", "password": "y"})
    assert response.status_code == 401
