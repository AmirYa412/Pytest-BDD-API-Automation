import json
from pytest_bdd import given, when
from pytest_bdd.parsers import parse


@when("client request comments of a post", target_fixture="post_comments_response")
def get_post_comments(client, post_data):
    post_id = post_data["id"]
    response = client.get_request(f"/posts/{post_id}/comments")
    return response
