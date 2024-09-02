from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Product, Order, OrderItem


class TestRegister(APITestCase):
    def test_register(self) -> None:
        url = reverse("register-user")
        data = {
            "username": "Omar",
            "password": "apitesting123",
            "email": "omar@gmail.com",
        }
        response = self.client.post(url, data, format="json")
        user = User.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)

        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])

    def test_register_existent_user(self) -> None:
        url = reverse("register-user")
        user1 = {
            "username": "Omar",
            "password": "apitesting123",
            "email": "omar@gmail.com",
        }
        user2 = {
            "username": "Omar",
            "password": "differentpass123",
            "email": "notomar@gmail.com",
        }
        response = self.client.post(url, user1, format="json")
        response2 = self.client.post(url, user2, format="json")
        user = User.objects.last()

        self.assertEqual(response.status_code, 201)  # 1st time registering
        self.assertEqual(response2.status_code, 400)  # 2nd time registering
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)

        self.assertEqual(user.username, user1["username"])
        self.assertEqual(user.email, user1["email"])

    def test_register_missing_email(self) -> None:
        url = reverse("register-user")
        data = {
            "username": "Omar",
            "password": "apitesting123",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)

    def test_register_missing_username(self) -> None:
        url = reverse("register-user")
        data = {
            "email": "Omar@gmail.com",
            "password": "apitesting123",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)

    def test_register_missing_password(self) -> None:
        url = reverse("register-user")
        data = {
            "username": "Omar",
            "email": "Omar@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)
