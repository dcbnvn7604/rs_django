from django.test import TestCase

from entry.models import Entry
from entry.views import EntryListView
from sr.tests import SRTestCaseInClient


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
