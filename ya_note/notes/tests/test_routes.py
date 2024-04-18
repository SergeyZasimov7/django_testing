from http import HTTPStatus

from .test_cases import (
    BaseTestCase, ADD_URL, HOME_URL, LIST_URL, LOGIN_URL, LOGOUT_URL,
    NOTE_EDIT_URL, NOTE_DELETE_URL, NOTE_DETAIL_URL,
    SIGNUP_URL, SUCCESS_URL
)


class TestContent(BaseTestCase):

    def check_status_codes(self, cases):
        for url, client, expected_status in cases:
            with self.subTest(url=url):
                response = client.get(url, follow_redirects=True)
                self.assertEqual(response.status_code, expected_status)
                if expected_status == HTTPStatus.FOUND:
                    self.assertTrue(response.location.endswith(SUCCESS_URL))

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
        self.check_status_codes(cases)
