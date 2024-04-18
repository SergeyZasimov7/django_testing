from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "url, client_fixture, expected_status",
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
    client_fixture,
    expected_status,
    request,
    author,
    not_author,
    comment_edit_url,
    comment_delete_url
):
    url = request.getfixturevalue(url)
    client = request.getfixturevalue(client_fixture)

    users = [author, not_author]
    statuses = [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

    for user, status in zip(users, statuses):
        client.force_login(user)
        for comment_url in (comment_edit_url, comment_delete_url):
            assert client.get(comment_url).status_code == status

    response = client.get(url)
    assert response.status_code == expected_status.value
