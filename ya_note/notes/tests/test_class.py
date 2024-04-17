from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note
from .test_urls import ADD_URL, NOTE_SLUG, NOTE_EDIT_URL, NOTE_DELETE_URL

User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls, create_note=False):
        cls.author = User.objects.create(username='автор')
        cls.not_author = User.objects.create(username='не автор')

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=NOTE_SLUG,
            author=cls.author,
        )

        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'novyij-zagolovok',
            'author': cls.author,
        }

        cls.url_add = ADD_URL
        cls.url_edit = NOTE_EDIT_URL
        cls.url_delete = NOTE_DELETE_URL
