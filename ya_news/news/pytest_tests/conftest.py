from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.test import Client

from news.models import News, Comment


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='не автор')


@pytest.fixture
def auth_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(news=news, author=author, text='Комментарий')


@pytest.fixture
def news_objects():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', kwargs={'pk': comment.pk})


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', kwargs={'pk': comment.pk})


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def comment_edit_redirect_url(login_url, comment_edit_url):
    return f'{login_url}?next={comment_edit_url}'


@pytest.fixture
def comment_delete_redirect_url(login_url, comment_delete_url):
    return f'{login_url}?next={comment_delete_url}'


@pytest.fixture
def ten_comments(news, author):
    comments = []
    for _ in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария'
        )
        comments.append(comment)
    return comments
