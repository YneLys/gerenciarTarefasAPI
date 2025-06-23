import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token
import bcrypt

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def register(client, username, password):
    return client.post("/register", json={"username": username, "password": password})

def login(client, username, password):
    return client.post("/login", json={"username": username, "password": password})

def test_register_and_login_success(client):
    # Registro
    resp = register(client, "alice", "1234")
    assert resp.status_code == 201

    # Login
    resp = login(client, "alice", "1234")
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()

def test_login_fail(client):
    # Tentativa de login sem registro
    resp = login(client, "ghost", "nopass")
    assert resp.status_code == 401
