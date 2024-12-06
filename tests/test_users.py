from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from api.models import LibUser


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = LibUser.objects.create(
            email="test@user.com", name="test user", active=True
        )

    def test_user_list(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "test user")

    def test_user_detail(self):
        response = self.client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test user")
        self.assertEqual(response.data["email"], "test@user.com")

    def test_create_user(self):
        data = {
            "email": "zhorny@acada.com",
            "name": "New user",
            "active": True,
        }
        response = self.client.post("/api/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "zhorny@acada.com")
        self.assertEqual(response.data["name"], "New user")

    def test_update_user(self):
        data = {"email": "updated@user.com", "name": "Updated User"}
        response = self.client.put(f"/api/users/{self.user.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updated@user.com")
        self.assertEqual(response.data["name"], "Updated User")

    def test_delete_user(self):
        response = self.client.delete(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LibUser.objects.get(id=self.user.id).active)
