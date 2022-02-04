# File for testing fastapi vote client services
from app import models
import pytest

# Create a fixture for adding a vote to a specific post for testing purposes
@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_user, test_posts):
    # Confirm successfully upvoting a post
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201
    assert res.json()['message'] == "successfully added vote"

def test_vote_twice_on_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
    assert res.json()['detail'] == f'User {test_user["id"]} has already voted on post {test_posts[3].id}'

def test_downvote_on_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
    assert res.json()['message'] == "successfully deleted vote"

def test_downvote_on_empty_post(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404
    assert res.json()['detail'] == "Vote does not exist"

def test_vote_on_nonexist_post(authorized_client, test_user):
    res = authorized_client.post("/vote/", json={"post_id": "1000", "dir": 1})
    assert res.status_code == 404
    assert res.json()['detail'] == 'Post with id 1000 does not exist'

def test_vote_unauth_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401


