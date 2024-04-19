import pytest
from http import HTTPStatus

@pytest.mark.parametrize(
    'url,
    client_fixture,
    expected_redirect,
    expected_status',
    [
        (pytest.lazy_fixture('home_url'), 'auth_client', False, HTTPStatus.OK),
        (pytest.lazy_fixture('detail_url'), 'auth_client', False, HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'), 'auth_client', False, HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'), 'auth_client', False, HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'), 'auth_client', False, HTTPStatus.OK),
        (
        pytest.lazy_fixture('comment_edit_url'),
        'auth_client',
        False,
        HTTPStatus.OK
        ),
        (
        pytest.lazy_fixture('comment_delete_url'),
        'auth_client',
        False,
        HTTPStatus.OK
        ),
        (pytest.lazy_fixture('comment_edit_url'), 'client', True, HTTPStatus.OK),
        (pytest.lazy_fixture('comment_delete_url'), 'client', True, HTTPStatus.OK),
])
def test_page_availability_and_redirect(url,
    client_fixture,
    expected_redirect,
    expected_status,
    auth_client,
    client,
    comment_edit_redirect_url,
    comment_delete_redirect_url
):
    if 'edit' in url:
        redirect_url = comment_edit_redirect_url
    elif 'delete' in url:
        redirect_url = comment_delete_redirect_url
    else:
        redirect_url = None

    if expected_redirect:
        response = client.get(url, follow=True)
        assert response.redirect_chain[0][0] == redirect_url
    else:
        response = auth_client.get(url)
        assert response.status_code == expected_status
