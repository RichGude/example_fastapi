# A special pytest file that allows defining any fixtures that will be accessible to any tests within this package (without importing)
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a test database for running all of the below commands
# Has the format 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest, by default, reruns the fixtures before each function ('function' scope). This is good practice.
@pytest.fixture
def session():
    # Reset the testing database at each run of the testing method
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # The SessionLocal is responsible for connecting to the database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # run code before the test finishes
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # Overside the Session dependency in each app method to point to test db, vice production
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    # anything after yield: run code after the test finishes
    pass

# In order to make every function isolated, identify a fixture for creating new users
@pytest.fixture
def test_user(client):
    user_data = {"email": "whatsup69@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "whatsup420@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    # Creating a user token just requires user_id
    return create_access_token({"user_id": test_user['id']})

# Create a new user credential that includes whether user is authenticated
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"}
    return client

# Create a fixture for generating test posts
@pytest.fixture
def test_posts(test_user, test_user2,  session):
    post_data = [{
            "title": "1st title",
            "content": "1st content",
            "owner_id": test_user['id']
        }, {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        }, {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        }, {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }]

    # Define a function for converting a dictionary to a Post model
    def create_post_model(post):
        return models.Post(**post)
    
    # Convert dictionary to models.Post element
    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    return session.query(models.Post).order_by(models.Post.id).all()