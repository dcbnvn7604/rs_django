from django.test import TestCase
from rest_framework import status

from entry.models import Entry
from entry.views import EntryListView
from sr.tests import SRTestCaseInClient, SRAPITestCase


class TestEntryListView(SRTestCaseInClient):
    def test_login_required(self):
        response = self.client.get('/entry/', follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/', fetch_redirect_response=False)

    def test_view(self):
        self._initial_user()

        self.client.post('/user/login/', {'username': 'test', 'password': 'testpw'}, follow=False)
        response = self.client.get('/entry/')
        self.assertEquals(response.status_code, 200)


class TestEntryCreateView(SRTestCaseInClient):
    def test_login_required(self):
        response = self.client.get('/entry/create/', follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/create/', fetch_redirect_response=False)

    def test_permission(self):
        self._login()

        response = self.client.get('/entry/create/', follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/create/', fetch_redirect_response=False)

    def test_view(self):
        self._login_user_in_group()

        response = self.client.get('/entry/create/', follow=False)
        self.assertEquals(response.status_code, 200)

    def test_create(self):
        self._login_user_in_group()

        response = self.client.post('/entry/create/', {'title': 'title', 'content': 'content'}, follow=False)
        self.assertRedirects(response, '/entry/', fetch_redirect_response=False)


class TestEntryUpdateView(SRTestCaseInClient):
    def setUp(self):
        super().setUp()

        self._initial_user()
        entry = Entry.objects.create(id=1, title='title1', content='content1', user=self.user)

    def test_login_required(self):
        response = self.client.post('/entry/1/', {'title': 'title 2', 'content': 'content 2'},follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/1/', fetch_redirect_response=False)

    def test_permission(self):
        self._login()

        response = self.client.post('/entry/1/', {'title': 'title 2', 'content': 'content 2'},follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/1/', fetch_redirect_response=False)

    def test_update(self):
        self._login_user_in_group()

        response = self.client.post('/entry/1/', {'title': 'title 2', 'content': 'content 2'},follow=False)
        self.assertRedirects(response, '/entry/', fetch_redirect_response=False)


class TestEntryDeleteView(SRTestCaseInClient):
    def setUp(self):
        super().setUp()

        self._initial_user()
        entry = Entry.objects.create(id=1, title='title1', content='content1', user=self.user)

    def test_login_required(self):
        response = self.client.post('/entry/1/delete/', follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/1/delete/', fetch_redirect_response=False)


    def test_permission(self):
        self._login()

        response = self.client.post('/entry/1/delete/', follow=False)
        self.assertRedirects(response, '/user/login/?next=/entry/1/delete/', fetch_redirect_response=False)

    def test_delete(self):
        self._login_user_in_group()

        response = self.client.post('/entry/1/delete/', follow=False)
        self.assertRedirects(response, '/entry/', fetch_redirect_response=False)


class TestEntryViewSetAPI(SRAPITestCase):
    def test_authentication(self):
        response = self.client.get('/api/entries/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        self._init_authen()

        response = self.client.get('/api/entries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_permission(self):
        self._init_authen()

        response = self.client.post('/api/entries/', {'title': 'title 2', 'content': 'content 2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        self._init_authen_in_group()

        response = self.client.post('/api/entries/', {'title': 'title 2', 'content': 'content 2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
