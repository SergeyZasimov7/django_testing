from http import HTTPStatus

import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def test_availability_for_comment_edit_and_delete(
        auth_client,
        user,
        not_author,
        comment_edit_url,
        comment_delete_url
):
    users = [user, not_author]
    statuses = [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
    for user, status in zip(users, statuses):
        auth_client.force_login(user)
        for url in (comment_edit_url, comment_delete_url):
            assert auth_client.get(url).status_code == status


def test_redirect_for_anonymous_client(
        client,
        login_url,
        comment_edit_url,
        comment_delete_url
):
    for url in (comment_edit_url, comment_delete_url):
        redirect_url = f'{login_url}?next={url}'
        response = client.get(url)
        assert response.url == redirect_url


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
def test_page_availability(url, client, expected_status, request):
    url = request.getfixturevalue(url)
    client = request.getfixturevalue(client)
    response = client.get(url)
    assert response.status_code == expected_status
