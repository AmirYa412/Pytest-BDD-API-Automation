from pytest_bdd import scenarios, then
from steps.posts_steps.steps import *

scenarios("../../features/posts.feature")


@then("verify response contain posts")
def verify_posts_response_data(posts_response):
    assert posts_response.status_code == 200
    response_data = posts_response.json()
    assert type(response_data) is list
    assert len(response_data) > 0


@then(parse("verify new post created with expected {title} and {body}"))
def verify_new_post_contain_expected_data(new_post_response, title, body):
    assert new_post_response.status_code == 201
    response_data = new_post_response.json()
    assert response_data["title"] == title
    assert response_data["body"] == body


@then("verify new post failed to create")
def verify_new_post_contain_expected_data(new_post_response):
    response_data = new_post_response.json()
    assert "title" not in response_data
    assert "body" not in response_data
