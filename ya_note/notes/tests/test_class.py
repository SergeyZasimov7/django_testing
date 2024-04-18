from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note

HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_URL = reverse('notes:add')

NOTE_SLUG = 'test-note'
NOTE_DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
NOTE_EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
NOTE_DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))

User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        }