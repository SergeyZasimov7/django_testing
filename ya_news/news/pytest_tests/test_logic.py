from http import HTTPStatus

import pytest

from news.models import Comment

COMMENT_FORM_DATA = {'text': 'Текст комментария'}


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data=COMMENT_FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(auth_client, news, user, detail_url):
    response = auth_client.post(detail_url, data=COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == user


def test_user_cant_use_bad_words(auth_client, detail_url, bad_words_data):
    response = auth_client.post(detail_url, data=bad_words_data)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(auth_client, comment_delete_url):
    initial_count = Comment.objects.count()
    response = auth_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_count - 1


def test_user_cant_delete_comment_of_another_user(
        reader_client,
        not_author,
        comment_delete_url
):
    initial_count = Comment.objects.count()
    reader_client.force_login(not_author)
    response = reader_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_count


def test_author_can_edit_comment(auth_client, comment, comment_edit_url):
    new_text = 'Измененный текст комментария'
    response = auth_client.post(comment_edit_url, data={'text': new_text})
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == new_text
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        comment,
        comment_edit_url
):
    response = reader_client.post(comment_edit_url, data=COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_FORM_DATA['text'], \
        "Текст комментария не соответствует ожидаемому значению"
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
