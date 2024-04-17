from django.urls import reverse

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
