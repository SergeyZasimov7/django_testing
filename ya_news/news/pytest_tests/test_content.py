import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, create_news_objects):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(news, client):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(news, client):
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(news, user, client):
    client.force_login(user)
    response = client.get(reverse('news:detail', kwargs={'pk': news.pk}))
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
