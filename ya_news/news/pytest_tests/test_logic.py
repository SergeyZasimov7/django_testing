from http import HTTPStatus

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_FORM_DATA = {'text': 'Текст комментария'}
COMMENT_EDIT_FORM_FIELDS = {'text': 'Измененный текст комментария'}
BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


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


def test_user_cant_use_bad_words(auth_client, detail_url):
    response = auth_client.post(detail_url, data=BAD_WORDS_DATA)
    assert Comment.objects.count() == 0
    assert response.context['form'].errors['text'][0] == WARNING


def test_author_can_delete_comment(auth_client, comment, comment_delete_url):
    initial_count = Comment.objects.count()
    response = auth_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_count - 1
    deleted_comment_exists = Comment.objects.filter(id=comment.pk).exists()
    assert not deleted_comment_exists


def test_user_cant_delete_comment_of_another_user(
        reader_client_not_author,
        comment_delete_url
):
    initial_comments = list(Comment.objects.all().values_list('id', flat=True))
    response = reader_client_not_author.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert initial_comments == list(Comment.objects.all().values_list(
        'id',
        flat=True
    ))


def test_author_can_edit_comment(auth_client, comment, comment_edit_url):
    response = auth_client.post(
        comment_edit_url,
        data=COMMENT_EDIT_FORM_FIELDS
    )
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_EDIT_FORM_FIELDS['text']
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
    assert updated_comment.text == COMMENT_FORM_DATA['text']
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
