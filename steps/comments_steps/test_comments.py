from pytest_bdd import scenarios, then
from steps.posts_steps.steps import *
from steps.comments_steps.steps import *

scenarios("../../features/comments.feature")


@then("verify post contain comments")
def verify_post_comments_data(post_comments_response, post_data):
    assert post_comments_response.status_code == 200
    response_data = post_comments_response.json()
    assert type(response_data) is list
    assert len(response_data) > 0



