from pytest_bdd import scenarios, then
from steps.posts_steps.steps import *

scenarios("../../features/posts.feature")


@then("verify response contain posts")
def verify_posts_response_data(posts_response):
    assert posts_response.status_code == 200
    response_data = posts_response.json()
    assert type(response_data) is list
    assert len(response_data) > 0


@then("verify post contain data")
def verify_post_contain_data(post_data):
    assert type(post_data["title"]) is str
    assert len(post_data["title"]) > 0
    assert type(post_data["title"]) is str
    assert len(post_data["title"]) > 0


@then(parse("verify new post created with expected {title} and {body}"))
def verify_new_post_contain_expected_data(new_post_response, title, body):
    assert new_post_response.status_code == 201
    response_data = new_post_response.json()
    assert response_data["title"] == title
    assert response_data["body"] == body


@then("verify new post failed to create")
def verify_new_post_creation_failed(new_post_response):
    # Expecting server to return status code 400
    assert new_post_response.status_code == 400
