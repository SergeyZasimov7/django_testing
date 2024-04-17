from http import HTTPStatus

from .test_urls import (
    ADD_URL, HOME_URL, LIST_URL, LOGIN_URL, LOGOUT_URL,
    NOTE_EDIT_URL, NOTE_DELETE_URL, NOTE_DETAIL_URL,
    SIGNUP_URL, SUCCESS_URL
)
from .test_class import BaseTestCase


class TestContent(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(create_note=True)

    def check_status_codes(self, cases):
        for url, client, expected_status in cases:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_pages_availability(self):
        cases = [
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
        ]
        self.check_status_codes(cases)

    def test_pages_availability_for_authenticated_user(self):
        cases = [
            (LIST_URL, self.client, HTTPStatus.OK),
            (SUCCESS_URL, self.client, HTTPStatus.OK),
            (ADD_URL, self.client, HTTPStatus.OK),
        ]
        for url, _, _ in cases:
            with self.subTest(url=url):
                self.assertEqual(
                    self.author_client.get(url).status_code, HTTPStatus.OK
                )

    def test_availability_for_notes_edit_and_delete(self):
        cases = [
            (self.author, HTTPStatus.OK),
            (self.not_author, HTTPStatus.NOT_FOUND),
        ]
        for user, status in cases:
            self.client.force_login(user)
            for url_name in [NOTE_EDIT_URL, NOTE_DETAIL_URL, NOTE_DELETE_URL]:
                with self.subTest(user=user, url_name=url_name):
                    self.assertEqual(
                        self.client.get(url_name).status_code, status
                    )

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
