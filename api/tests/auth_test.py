from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):

    def setUp(self):

        url = reverse("signup")
        data = {"username": "teste1", "password": "teste1"}
        self.client.post(url, data)
        self.token = Token.objects.first().key

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

    def test_login_user(self):
        url = reverse("login")
        data = {"username": "teste1", "password": "teste1"}
        response = self.client.post(url, data)
        self.assertEqual(response.data, {"Token": self.token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_try_login_and_raise_error_user_or_password(self):
        expected = {
            "error": "Invalid Email or Password",
        }
        url = reverse("login")
        data = {"username": "123", "password": "1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_try_login_and_raise_bad_resquest(self):
        expected = {
            "error": "Bad request",
        }
        url = reverse("login")
        data = {"teste": "123", "teste": "1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
