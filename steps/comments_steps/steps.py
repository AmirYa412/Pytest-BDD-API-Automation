import json
from pytest_bdd import given, when
from pytest_bdd.parsers import parse


@when("client request comments of a post", target_fixture="post_comments_response")
def get_post_comments(client, post_data):
    post_id = post_data["id"]
    response = client.get_request(f"/posts/{post_id}/comments")
    return response


@when(parse("client publish new comment with {name}, {email} and {body}"), target_fixture="new_comment_response")
def create_new_comment(client, post_data, name, email, body):
    data = json.dumps({
        "postId": post_data["id"],
        "email": email,
        "name": name,
        "body": body
    })
    response = client.post_request("/comments", data=data)
    return response
