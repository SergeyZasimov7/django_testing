from notes.forms import NoteForm
from .test_urls import LIST_URL, ADD_URL, NOTE_EDIT_URL
from .test_class import BaseTestCase


class TestContent(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(create_note=True)

    def test_forms_passed_to_create_and_edit_notes_page(self):
        urls = [ADD_URL, NOTE_EDIT_URL]
        for url in urls:
            response = self.author_client.get(url)
            self.assertIsNotNone(response.context['form'])
            self.assertIsInstance(response.context['form'], NoteForm)

    def test_individual_note_passed_to_notes_list(self):
        response = self.author_client.get(LIST_URL)
        self.assertIn(self.note, response.context['object_list'])
        note_from_context = response.context['object_list'][0]
        self.assertEqual(self.note.title, note_from_context.title)
        self.assertEqual(self.note.text, note_from_context.text)
        self.assertEqual(self.note.slug, note_from_context.slug)
        self.assertEqual(self.note.author, note_from_context.author)

    def test_notes_of_other_users_not_passed_to_notes_list(self):
        response = self.not_author_client.get(LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])
