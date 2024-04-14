from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from notes.models import Note


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='sergey')
        cls.reader = User.objects.create(username='reader')
        cls.note = Note.objects.create(
            title='Примечание',
            text='Текст',
            slug='test-note',
            author=cls.author
        )

    def test_pages_availability(self):
        urls = (
            ('notes:home'),
            ('users:login'),
            ('users:logout'),
            ('users:signup'),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_authenticated_user(self):
        urls = [
            ('notes:list'),
            ('notes:success'),
            ('notes:add'),
        ]

        for name in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:detail', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls_without_slug = ['notes:add', 'notes:list', 'notes:success']
        urls_with_slug = ['notes:edit', 'notes:detail', 'notes:delete']

        login_url = reverse('users:login')

        for url_name in urls_with_slug:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

        for url_name in urls_without_slug:
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
