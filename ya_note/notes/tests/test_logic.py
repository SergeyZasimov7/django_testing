from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note
from .test_cases import (
    BaseTestCase, ADD_URL, SUCCESS_URL, NOTE_DELETE_URL, NOTE_EDIT_URL
)


User = get_user_model()


class TestContent(BaseTestCase):

    def get_updated_form_data(self, **kwargs):
        return {**self.form_data, **kwargs}

    def test_not_unique_slug(self):
        initial_note_count = Note.objects.get(slug=self.note.slug)
        response = self.author_client.post(ADD_URL, data={
            **self.form_data,
            'slug': self.note.slug
        })
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(
            initial_note_count,
            Note.objects.get(slug=self.note.slug)
        )

    def test_create_note_with_full_form_data(self):
        Note.objects.all().delete()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get(slug=self.form_data.get('slug', None))
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_create_note_with_slug(self):
        Note.objects.all().delete()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        form_data = self.get_updated_form_data(slug='edited-slug')
        response = self.author_client.post(NOTE_EDIT_URL, form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, form_data['title'])
        self.assertEqual(self.note.text, form_data['text'])
        self.assertEqual(self.note.slug, form_data['slug'])
        self.assertEqual(self.note.author, self.author)

    def test_other_user_cant_edit_note(self):
        original_title, original_text, original_slug = (
            self.note.title,
            self.note.text,
            self.note.slug
        )
        form_data = self.get_updated_form_data(slug='edited-slug')
        response = self.not_author_client.post(NOTE_EDIT_URL, form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, original_title)
        self.assertEqual(self.note.text, original_text)
        self.assertEqual(self.note.slug, original_slug)
        self.assertEqual(self.note.author, self.author)

    def test_author_can_delete_note(self):
        response = self.author_client.post(NOTE_DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.not_author_client.post(NOTE_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
