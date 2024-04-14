from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_availability_for_comment_edit_and_delete(
    auth_client,
    user,
    not_author,
    comment
     ):
    users = [user, not_author]
    statuses = [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
    for user, status in zip(users, statuses):
        auth_client.force_login(user)
        for name in ('news:edit', 'news:delete'):
            url = reverse(name, args=(comment.id,))
            response = auth_client.get(url)
            assert response.status_code == status


@pytest.mark.django_db
def test_redirect_for_anonymous_client(client, comment):
    login_url = reverse('users:login')
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        redirect_url = f'{login_url}?next={url}'
        response = client.get(url)
        assert response.url == redirect_url


@pytest.mark.django_db
def test_pages_availability(auth_client, news):
    urls = [
        ('news:home', None),
        ('news:detail', (news.id,)),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ]
    for name, args in urls:
        url = reverse(name, args=args)
        response = auth_client.get(url)
        assert response.status_code == HTTPStatus.OK
