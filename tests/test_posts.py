# File for testing fastapi post client services
from app import schemas
from app.config import settings
from jose import jwt
from typing import List
import pytest

#%# Get Post(s) Testing
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # The res object returns a list of PostOut objects - more testing can occur

    # Validate the schemas of the posts
    def validate(post):
        return schemas.PostVote(**post)
    posts_list = list(map(validate, res.json()))
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id

def test_unauth_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    # Since non-logged-in users can get all posts, status should still be same 200
    assert res.status_code == 200

def test_unauth_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200

def test_unauth_get_one_nonexist_post(client):
    res = client.get('/posts/1000')
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostVote(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

def test_get_one_nonexist_post(authorized_client):
    res = authorized_client.get('/posts/1000')
    assert res.status_code == 404

#%# Create Post Testing
@pytest.mark.parametrize("title, content, published, status_code", [
    ("new title", "new content", True, 201),
    ("more title", "more content", False, 201),
    (None, "new content", True, 422),
    ("Some title", None, True, 422)
])
def test_create_post(authorized_client, test_user, title, content, published, status_code):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    if res.status_code == 201:
        post = schemas.PostResponse(**res.json())
        assert post.title == title
        assert post.content == content
        assert post.published == published
        assert post.owner_id == test_user['id']
    
    assert res.status_code == status_code

def test_unauth_user_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "some title", "content": "some content", "published": False})
    assert res.status_code == 401

#%# Delete Post Testing
def test_unauth_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    old_len = len(test_posts)
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    new_len = len(authorized_client.get("/posts/").json())

    assert res.status_code == 204
    assert new_len == old_len - 1

def test_delete_nonexist_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/1000")
    assert res.status_code == 404

# Test is an authorized user attempts to delete another user's post (not allowed)
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    # The fourth post belongs to a second user
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

#%# Update Post Testing
@pytest.mark.parametrize("title, content, published, status_code", [
    ("updated title", "updated content", False, 201),
    ("other title", "other content", None, 201),
    (None, "Some content", True, 422),
    ("Some title", None, False, 422)
])
def test_update_post(authorized_client, test_user, test_posts, title, content, published, status_code):
    data = {
        "title": title,
        "content": content,
        "published": published}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    if res.status_code == 200:
        post = schemas.PostResponse(**res.json())
        assert post.title == title
        assert post.content == content
        assert post.published == published
        assert post.owner_id == test_user['id']
    else:
        assert res.status_code == 422

def test_unauth_update_post(client, test_user, test_posts):
    data = {
        "title": "some title",
        "content": "some content"}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_nonexist_post(authorized_client, test_user, test_posts):
    data = {
        "title": "some title",
        "content": "some content"}
    res = authorized_client.put("/posts/1000", json=data)
    assert res.status_code == 404

# Test is an authorized user attempts to update another user's post (not allowed)
def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "some title",
        "content": "some content"}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


    