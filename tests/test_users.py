# File for testing fastapi user client services
from app import schemas
from app.config import settings
from jose import jwt
import pytest


def test_create_user(client):
    # The post route requires a Users schema (email & password) to be sent with the request
    res = client.post("/users/", json={'email': 'hello123@gmail.com', 'password': 'password123'})

    # We can confirm the output has the correct schema (not having the right would )
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    # Out should have the UserOut schema ('id', 'email', and 'created_at')
    assert new_user.email == 'hello123@gmail.com'

def test_login_user(client, test_user):
    # The post route sends data in a form-data format
    res = client.post("/login", data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res. token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong_email@gmail.com', 'password123', 403),
    ('hello123@gmail.com', 'wrong_password', 403),
    ('wrng_email@gmail.com', 'wrg_password', 403),
    (None, 'password123', 422),
    ('hello123@gmail.com', None, 422)])
def test_failed_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == 'Invalid Credentials'