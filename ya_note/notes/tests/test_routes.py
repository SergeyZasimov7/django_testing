from http import HTTPStatus

from .test_cases import (
    BaseTestCase, ADD_URL, HOME_URL, LIST_URL, LOGIN_URL, LOGOUT_URL,
    NOTE_EDIT_URL, NOTE_DELETE_URL, NOTE_DETAIL_URL,
    SIGNUP_URL, SUCCESS_URL
)


class TestContent(BaseTestCase):

    def test_pages_availability_and_auth_notes(self):
        cases = [
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.author_client, HTTPStatus.OK),
            (ADD_URL, self.author_client, HTTPStatus.OK),
            (NOTE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (NOTE_EDIT_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (NOTE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (NOTE_DETAIL_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (NOTE_DELETE_URL, self.author_client, HTTPStatus.OK),
            (NOTE_DELETE_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
        ]

        for url, client, expected_status in cases:
            with self.subTest(url=url):
                response = client.get(url, follow_redirects=True)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        urls_without_slug = [ADD_URL, LIST_URL, SUCCESS_URL]
        urls_with_slug = [NOTE_EDIT_URL, NOTE_DETAIL_URL, NOTE_DELETE_URL]
        login_url = LOGIN_URL
        cases = [
            (url, self.client, f'{login_url}?next={url}')
            for url in urls_with_slug + urls_without_slug
        ]
        for url, _, redirect_url in cases:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect_url)
