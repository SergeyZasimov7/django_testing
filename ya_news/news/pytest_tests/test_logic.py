from http import HTTPStatus

import pytest
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(auth_client, news, form_data, user):
    url = reverse('news:detail', args=(news.id,))
    response = auth_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.first()
    assert comment.text == 'Текст комментария'
    assert comment.news == news
    assert comment.author == user


@pytest.mark.django_db
def test_user_cant_use_bad_words(auth_client, news):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_client.post(url, data=bad_words_data)
    assert 'form' in response.context
    assert 'text' in response.context['form'].errors
    assert response.context['form'].errors['text'][0] == WARNING
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(auth_client, news, user):
    comment = Comment.objects.create(
        text='Комментарий',
        news=news,
        author=user)
    url = reverse('news:delete', kwargs={'pk': comment.pk})
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    reader_client,
    news,
    user,
    not_author
     ):
    comment = Comment.objects.create(
        text='Другой комментарий',
        news=news,
        author=user
    )
    reader_client.force_login(not_author)
    url = reverse('news:delete', kwargs={'pk': comment.pk})
    response = reader_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_author_can_edit_comment(auth_client, news, user):
    comment = Comment.objects.create(
        text='Старый комментарий',
        news=news,
        author=user)
    url = reverse('news:edit', kwargs={'pk': comment.pk})
    response = auth_client.post(url, data={'text': 'Новый текст комментария'})
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == 'Новый текст комментария'


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    reader_client, news, form_data, not_author
     ):
    comment = Comment.objects.create(
        author=not_author,
        news=news,
        text="Оригинальный текст комментария"
        )
    assert Comment.objects.exists()
    response = reader_client.post(
        reverse('news:edit', kwargs={'pk': comment.pk}),
        data=form_data
        )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.first()
    if comment:
        assert comment.text == 'Оригинальный текст комментария'
    else:
        assert False, "Комментарий не существует"
