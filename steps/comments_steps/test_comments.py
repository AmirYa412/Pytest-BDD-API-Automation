from pytest_bdd import scenarios, then
from steps.posts_steps.steps import *
from steps.comments_steps.steps import *

scenarios("../../features/comments.feature")


@then("verify post contain comments")
def verify_post_contain_comments(post_comments_response, post_data):
    assert post_comments_response.status_code == 200
    response_data = post_comments_response.json()
    assert type(response_data) is list
    assert len(response_data) > 0


@then(parse("verify new comment published with {name}, {email} and {body}"))
def verify_new_comment_response(post_data, new_comment_response, name, email, body):
    assert new_comment_response.status_code == 201
    response_data = new_comment_response.json()
    assert response_data["postId"] == post_data["id"]
    assert response_data["email"] == email
    assert response_data["name"] == name
    assert response_data["body"] == body

