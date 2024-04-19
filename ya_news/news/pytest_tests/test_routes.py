from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.parametrize('url, client_fixture, expected_status', [
    ('news:home', 'auth_client', HTTPStatus.OK),
    ('news:detail', 'auth_client', HTTPStatus.OK),
    ('users:login', 'auth_client', HTTPStatus.OK),
    ('users:logout', 'auth_client', HTTPStatus.OK),
    ('users:signup', 'auth_client', HTTPStatus.OK),
    ('news:edit', 'auth_client', HTTPStatus.NOT_FOUND),
    ('news:delete', 'auth_client', HTTPStatus.NOT_FOUND),
])
def test_pages_availability(
    url,
    client_fixture,
    expected_status,
    news,
    request
):
    client = request.getfixturevalue(client_fixture)
    if url in ('news:detail', 'news:edit', 'news:delete'):
        response = client.get(reverse(url, args=(news.id,)))
    else:
        response = client.get(reverse(url))
    assert response.status_code == expected_status


@pytest.mark.parametrize('url, client_fixture, expected_redirect', [
    ('news:edit', 'client', True),
    ('news:delete', 'client', True),
])
def test_redirect_for_anonymous_client(
    url,
    client_fixture,
    login_url,
    expected_redirect,
    comment,
    request
):
    client = request.getfixturevalue(client_fixture)
    url = reverse(url, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url, follow=True)
    assert response.redirect_chain[0][0] == redirect_url
