from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(TestCase):
    COMMENT_TEXT = 'Текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='автор')
        cls.not_author = User.objects.create(username='не автор')

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
        }

        cls.url_add = reverse('notes:add')
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.note.slug,))

    def test_not_unique_slug(self):
        response = self.author_client.post(self.url_add, data={
            **self.form_data,
            'slug': self.note.slug
        })
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        Note.objects.all().delete()
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        form_data = {**self.form_data, 'slug': 'edited-slug'}
        response = self.author_client.post(self.url_edit, form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, form_data['title'])
        self.assertEqual(self.note.text, form_data['text'])
        self.assertEqual(self.note.slug, form_data['slug'])

    def test_other_user_cant_edit_note(self):
        form_data = {**self.form_data, 'slug': 'edited-slug'}
        response = self.not_author_client.post(self.url_edit, form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Заголовок')
        self.assertEqual(self.note.text, 'Текст заметки')
        self.assertEqual(self.note.slug, 'note-slug')

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.url_delete)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.not_author_client.post(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
