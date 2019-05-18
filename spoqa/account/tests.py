import json

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class Tests0000Account(APITestCase):
    data = {
        'username': '염석준',
        'nickname': 'seokjun',
        'password': '@test1234',
    }

    def test_0000_sign_up(self):
        url = reverse('account:registration')
        response = self.client.post(url, self.data, format='json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=response_data['id'])

        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['nickname'], user.nickname)
        self.assertTrue(user.check_password(self.data['password']))

    def test_0001_sign_in(self):
        user = User.objects.create_user(**self.data)

        is_login_url = reverse('account:is-login')
        response = self.client.get(is_login_url)
        response_data = json.loads(response.content)

        self.assertFalse(response_data['is_login'])

        login_url = reverse('account:login')
        response = self.client.post(login_url, self.data, format='json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.id, response_data['id'])

        response = self.client.get(is_login_url)
        response_data = json.loads(response.content)

        self.assertTrue(response_data['is_login'])

        logout_url = reverse('account:logout')
        response = self.client.get(logout_url)

        response = self.client.get(is_login_url)
        response_data = json.loads(response.content)

        self.assertFalse(response_data['is_login'])
