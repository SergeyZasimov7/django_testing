from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from notes.models import Note


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='автор')
        cls.reader = User.objects.create(username='не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test-note',
            author=cls.author
        )

    def test_forms_passed_to_create_notes_page(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:add'))
        self.assertIsNotNone(response.context['form'])

    def test_forms_passed_to_edit_notes_page(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse(
            'notes:edit',
            kwargs={'slug': self.note.slug}
        ))
        self.assertIsNotNone(response.context['form'])

    def test_individual_note_passed_to_notes_list(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_of_other_users_not_passed_to_notes_list(self):
        self.client.force_login(self.reader)
        other_note = Note.objects.create(
            title='Другой заголовок',
            text='Другой текст',
            slug='another-note',
            author=self.author
        )
        response = self.client.get(reverse('notes:list'))
        self.assertNotIn(other_note, response.context['object_list'])
