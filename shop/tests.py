from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Product, Order, OrderItem


class TestRegisterAPIs(APITestCase):
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


class TestLoginAPIs(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "omar",
            "password": "testing12345",
            "email": "omar@gmail.com",
        }
        self.login_url = reverse("login")
        self.register_url = reverse("register-user")

    def test_login(self) -> None:
        self.client.post(self.register_url, self.data, format="json")
        token = Token.objects.last()

        login_cred = {
            "username": "omar",
            "password": "testing12345",
        }
        response = self.client.post(self.login_url, login_cred, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(token.key, response.data["token"])

    def test_login_missing_credentials(self) -> None:
        self.client.post(self.register_url, self.data, format="json")
        login_cred = {}
        response = self.client.post(self.login_url, login_cred, format="json")

        self.assertEqual(response.status_code, 400)

    def test_login_missing_username(self) -> None:
        self.client.post(self.register_url, self.data, format="json")
        login_cred = {
            "password": "testing12345",
        }
        response = self.client.post(self.login_url, login_cred, format="json")

        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self) -> None:
        self.client.post(self.register_url, self.data, format="json")
        login_cred = {
            "username": "omar",
        }
        response = self.client.post(self.login_url, login_cred, format="json")

        self.assertEqual(response.status_code, 400)


class TestProductAPIs(APITestCase):
    def setUp(self) -> None:
        # admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin"
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # regular user
        self.regular_user = User.objects.create_user(username="user", password="user")
        self.regular_token = Token.objects.create(user=self.regular_user)

        self.url_list_create = reverse("list-create-products")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test description",
            price="100.00",
            stock=10,
        )
        self.url_update_delete = reverse(
            "update-delete-retrieve-products", args=[self.product.id]
        )

    def test_product_create_by_admin(self):
        product_data = {
            "name": "Backpack",
            "description": "description for backpack",
            "price": "250.00",
            "stock": 44,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.post(self.url_list_create, product_data, format="json")

        self.assertEqual(response.status_code, 201)

    def test_product_create_by_non_admin(self):
        product_data = {
            "name": "Backpack",
            "description": "description for backpack",
            "price": "250.00",
            "stock": 44,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.post(self.url_list_create, product_data, format="json")

        self.assertEqual(response.status_code, 403)

    def test_product_update_by_admin(self):
        update_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": "200.00",
            "stock": 30,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.put(self.url_update_delete, update_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_product_update_by_non_admin(self):
        update_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": "200.00",
            "stock": 30,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.put(self.url_update_delete, update_data, format="json")

        self.assertEqual(response.status_code, 403)

    def test_product_delete_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.delete(self.url_update_delete)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertEqual(Product.objects.count(), 0)

    def test_product_delete_by_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.delete(self.url_update_delete)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 1)
