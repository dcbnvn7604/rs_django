from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test import Client
from rest_framework.test import APITestCase


class SRTestMixin:
    user = None

    def _initial_user(self):
        if not self.user:
            self.user = User.objects.create_user(username='test', email='test@mail.com', password='testpw')

    def _join_group(self):
        if self.user:
            group = Group.objects.get(name='editor') 
            self.user.groups.add(group)


class SRTestCaseInClient(SRTestMixin, TestCase):
    def _login(self):
        self._initial_user()
        self.client.post('/user/login/', {'username': 'test', 'password': 'testpw'}, follow=False)

    def _login_user_in_group(self):
        self._login()
        self._join_group()

    def setUp(self):
        self.client = Client()


class SRAPITestCase(SRTestMixin, APITestCase):
    def _init_authen(self):
        self._initial_user()

        response = self.client.post('/api/auth/', {'username': 'test', 'password': 'testpw'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def _init_authen_in_group(self):
        self._init_authen()
        self._join_group()


class TestAuthentication(SRTestCaseInClient):
    def test_login_logout(self):
        self._initial_user()

        response = self.client.post('/user/login/', {'username': 'test', 'password': 'testpw'})
        self.assertRedirects(response, '/entry/')
        response = self.client.get('/user/logout/')
        self.assertRedirects(response, '/user/login/')


class TestAuthenticationAPI(SRTestMixin, APITestCase):
    def test_auth_fail(self):
        response = self.client.post('/api/auth/', {'username': 'test', 'password': 'testpw'})
        self.assertEquals(response.status_code, 400)

    def test_auth(self):
        self._initial_user()

        response = self.client.post('/api/auth/', {'username': 'test', 'password': 'testpw'})
        self.assertEquals(response.status_code, 200)
