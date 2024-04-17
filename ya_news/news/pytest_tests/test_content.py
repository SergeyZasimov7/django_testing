import pytest

from django.conf import settings

from news.forms import CommentForm


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def test_news_count(client, news_objects, home_url):
    response = client.get(home_url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url):
    all_dates = [
        news.date for news in client.get(home_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(news, client, detail_url):
    response = client.get(detail_url)
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all(all_timestamps[i] >= all_timestamps[i+1] for i in range(
        len(all_timestamps)-1
    ))


def test_anonymous_client_has_no_form(news, client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(news, user, client, detail_url):
    client.force_login(user)
    response = client.get(detail_url)
    form = response.context.get('form')
    assert 'form' in response.context and isinstance(form, CommentForm)
