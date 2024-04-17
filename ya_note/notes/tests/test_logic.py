from http import HTTPStatus

from django.contrib.auth import get_user_model


from notes.forms import WARNING
from notes.models import Note
from .test_class import BaseTestCase
from .test_urls import SUCCESS_URL


User = get_user_model()


class TestContent(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(create_note=True)

    def get_updated_form_data(self, **kwargs):
        return {**self.form_data, **kwargs}

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
        self.assertEqual(Note.objects.filter(pk=self.note.pk).exists(), True)

    def test_create_note_with_full_form_data(self):
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_empty_slug(self):
        Note.objects.all().delete()
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_author_can_edit_note(self):
        form_data = self.get_updated_form_data(slug='edited-slug')
        response = self.author_client.post(self.url_edit, form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, form_data['title'])
        self.assertEqual(self.note.text, form_data['text'])
        self.assertEqual(self.note.slug, form_data['slug'])
        self.assertEqual(self.note.author, self.form_data['author'])

    def test_other_user_cant_edit_note(self):
        original_title = self.note.title
        original_text = self.note.text
        original_slug = self.note.slug
        form_data = self.get_updated_form_data(slug='edited-slug')
        response = self.not_author_client.post(self.url_edit, form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, original_title)
        self.assertEqual(self.note.text, original_text)
        self.assertEqual(self.note.slug, original_slug)
        self.assertEqual(self.note.author, self.form_data['author'])

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.url_delete)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.not_author_client.post(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.filter(pk=self.note.pk).exists(), True)
