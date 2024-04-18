from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, news_objects, home_url):
    response = client.get(home_url)
    assert response.context['object_list'].count() == \
        settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url):
    all_dates = [
        news.date for news in client.get(home_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps, reverse=True)


def test_anonymous_client_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(auth_client, detail_url):
    response = auth_client.get(detail_url)
    form = response.context.get('form')
    assert 'form' in response.context and isinstance(form, CommentForm)
