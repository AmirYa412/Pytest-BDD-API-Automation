import json
import random
from pytest_bdd import given, when
from pytest_bdd.parsers import parse


@given("client request all posts", target_fixture="posts_response")
def get_all_posts(client):
    response = client.get_request("/posts")
    return response


@when("client choose a random post", target_fixture="post_data")
def get_random_post(posts_response):
    response_data = posts_response.json()
    random_post_data = random.choice(response_data)
    return random_post_data


@given(parse("client create new post with {title} and {body}"), target_fixture="new_post_response")
def create_new_post(client, title, body):
    data = json.dumps({
        "title": title,
        "body": body
    })
    response = client.post_request("/posts", data=data)
    return response


@given("client create new post with missing data", target_fixture="new_post_response")
def create_invalid_post(client):
    response = client.post_request("/posts", data=None)
    return response
