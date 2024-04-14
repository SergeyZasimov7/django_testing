from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test import Client

from news.models import News, Comment


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='не автор')


@pytest.fixture
def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def reader_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def comment(news, user):
    return Comment.objects.create(news=news, author=user, text='Комментарий')


@pytest.fixture
def create_news_objects():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}
