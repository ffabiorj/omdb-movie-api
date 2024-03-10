from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):

    def test_create_login(self):
        url = reverse("signup")
        data = {"username": "teste", "password": "teste"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"user": "teste"})
        self.assertTrue(User.objects.exists())

    def test_try_create_login_and_raise_bad_resquest(self):
        url = reverse("signup")
        response = self.client.post(url, {"test": "teste"})
        self.assertEqual(response.data, {"error": "Bad request"})
