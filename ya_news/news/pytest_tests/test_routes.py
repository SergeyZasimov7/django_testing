import pytest
from http import HTTPStatus


@pytest.mark.parametrize('url, client_fixture, expected_status', [
    (pytest.lazy_fixture('home_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('detail_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('login_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('logout_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('signup_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('comment_edit_url'), 'auth_client', HTTPStatus.OK),
    (pytest.lazy_fixture('comment_delete_url'), 'auth_client', HTTPStatus.OK),
])
def test_pages_availability(
        url,
        client_fixture,
        expected_status,
        news,
        request,
):
    client = request.getfixturevalue(client_fixture)
    if 'edit' in url or 'delete' in url:
        response = client.get(url)
    else:
        response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('url, client_fixture, expected_redirect', [
    (pytest.lazy_fixture('comment_edit_url'), 'client', True),
    (pytest.lazy_fixture('comment_delete_url'), 'client', True),
])
def test_redirect_for_anonymous_client(
        url,
        client_fixture,
        login_url,
        expected_redirect,
        comment,
        request,
):
    client = request.getfixturevalue(client_fixture)
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url, follow=True)
    assert response.redirect_chain[0][0] == redirect_url
