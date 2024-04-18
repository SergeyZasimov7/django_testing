from notes.forms import NoteForm
from .test_cases import BaseTestCase, LIST_URL, ADD_URL, NOTE_EDIT_URL


class TestContent(BaseTestCase):

    def test_form_passed_to_create_note_page(self):
        response = self.author_client.get(ADD_URL)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_passed_to_edit_note_page(self):
        response = self.author_client.get(NOTE_EDIT_URL)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_individual_note_passed_to_notes_list(self):
        response = self.author_client.get(LIST_URL)
        object_list = response.context['object_list']
        self.assertTrue(object_list)
        self.assertEqual(len(object_list), 1)
        note = object_list[0]
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_notes_of_other_users_not_passed_to_notes_list(self):
        self.assertNotIn(
            self.note,
            self.not_author_client.get(LIST_URL).context['object_list']
        )
