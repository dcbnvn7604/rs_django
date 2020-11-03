from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class TestAuthentication(TestCase):
    def test_login_logout(self):
        self.user = User.objects.create_user(username='test', email='test@mail.com', password='testpw')
        client = Client()
        response = client.post('/user/login/', {'username': 'test', 'password': 'testpw'})
        self.assertRedirects(response, '/entry/')
        response = client.get('/user/logout/')
        self.assertRedirects(response, '/user/login/')
