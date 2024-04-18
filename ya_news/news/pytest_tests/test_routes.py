from http import HTTPStatus

import pytest


def test_redirect_for_anonymous_client(
        client,
        comment_edit_redirect_url,
        comment_delete_redirect_url,
        comment_edit_url,
        comment_delete_url
):
    response_edit = client.get(comment_edit_url)
    assert response_edit.url == comment_edit_redirect_url
    response_delete = client.get(comment_delete_url)
    assert response_delete.url == comment_delete_redirect_url


@pytest.mark.parametrize(
    "url, client, expected_status",
    [
        ('home_url', 'auth_client', HTTPStatus.OK),
        ('detail_url', 'auth_client', HTTPStatus.OK),
        ('login_url', 'auth_client', HTTPStatus.OK),
        ('logout_url', 'auth_client', HTTPStatus.OK),
        ('signup_url', 'auth_client', HTTPStatus.OK),
    ]
)
def test_page_availability(
    url,
    client,
    expected_status,
    request,
    user,
    not_author,
    comment_edit_url,
    comment_delete_url
):
    url = request.getfixturevalue(url)
    client = request.getfixturevalue(client)

    users = [user, not_author]
    statuses = [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

    for user, status in zip(users, statuses):
        client.force_login(user)
        for comment_url in (comment_edit_url, comment_delete_url):
            assert client.get(comment_url).status_code == status

    response = client.get(url)
    assert response.status_code == expected_status
