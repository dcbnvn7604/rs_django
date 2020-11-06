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
        self._login()

        response = self.client.get('/entry/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        self._login()

        Entry.objects.create(id=1, title='title1', content='content1', user=self.user)
        Entry.objects.create(id=2, title='abc', content='content2', user=self.user)

        response = self.client.get('/entry/?q=abc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['entry_list']), 1)


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
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        self._login_user_in_group()

        response = self.client.post('/entry/create/', {'title': 'title', 'content': 'content'}, follow=False)
        self.assertRedirects(response, '/entry/', fetch_redirect_response=False)


class TestEntryUpdateView(SRTestCaseInClient):
    def setUp(self):
        super().setUp()

        self._initial_user()
        Entry.objects.create(id=1, title='title1', content='content1', user=self.user)

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
        Entry.objects.create(id=1, title='title1', content='content1', user=self.user)

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
    def setUp(self):
        super().setUp()

        self._initial_user()
        Entry.objects.create(id=1, title='title1', content='content1', user=self.user)

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

    def test_update_permission(self):
        self._init_authen()

        response = self.client.put('/api/entries/1/', {'title': 'title 2', 'content': 'content 2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        self._init_authen_in_group()

        response = self.client.put('/api/entries/1/', {'title': 'title 2', 'content': 'content 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_permission(self):
        self._init_authen()

        response = self.client.delete('/api/entries/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        self._init_authen_in_group()

        response = self.client.delete('/api/entries/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search(self):
        self._init_authen()

        Entry.objects.create(id=2, title='abc', content='content2', user=self.user)

        response = self.client.get('/api/entries/?q=abc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestGraphql(SRAPITestCase):
    def setUp(self):
        super().setUp()

        self._initial_user()
        Entry.objects.create(id=2, title='title1', content='content1', user=self.user)

    def test_authentication(self):
        query = '''
            query {
                entries {
                    id
                    title
                    content
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['entries'])

    def test_entries(self):
        self._init_authen()

        query = '''
            query {
                entries {
                    id
                    title
                    content
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['data']['entries'][0]['id'], '2')

    def test_create_authentication(self):
        query = '''
            mutation {
                createEntry(title: "title 2", content: "content 2") {
                    entry {
                        id
                    }
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['createEntry'])

    def test_create_permission(self):
        self._init_authen()

        query = '''
            mutation {
                createEntry(title: "title 2", content: "content 2") {
                    entry {
                        id
                    }
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['createEntry'])

    def test_create(self):
        self._init_authen_in_group()

        query = '''
            mutation {
                createEntry(title: "title 2", content: "content 2") {
                    entry {
                        id
                    }
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertTrue(response['data']['createEntry']['ok'])

    def test_update_authentication(self):
        query = '''
            mutation {
                updateEntry(id: 2, title: "title 2", content: "content 2") {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['updateEntry'])

    def test_update_permission(self):
        self._init_authen()

        query = '''
            mutation {
                updateEntry(id:2, title: "title 2", content: "content 2") {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['updateEntry'])

    def test_update(self):
        self._init_authen_in_group()

        query = '''
            mutation {
                updateEntry(id: 2, title: "title 1", content: "content 1") {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertTrue(response['data']['updateEntry']['ok'])

    def test_update_fail(self):
        self._init_authen_in_group()

        query = '''
            mutation {
                updateEntry(id: 1, title: "title 1", content: "content 1") {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertFalse(response['data']['updateEntry']['ok'])

    def test_delete_authentication(self):
        query = '''
            mutation {
                deleteEntry(id: 2) {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['deleteEntry'])

    def test_delete_permission(self):
        self._init_authen()

        query = '''
            mutation {
                deleteEntry(id: 2) {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNone(response['data']['deleteEntry'])

    def test_delete(self):
        self._init_authen_in_group()

        query = '''
            mutation {
                deleteEntry(id: 2) {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertTrue(response['data']['deleteEntry']['ok'])

    def test_delete_fail(self):
        self._init_authen_in_group()

        query = '''
            mutation {
                deleteEntry(id: 1) {
                    ok
                }
            }
        '''
        response = self.client.post('/graphql/', {"query": query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertFalse(response['data']['deleteEntry']['ok'])
