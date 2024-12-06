from django.test import TestCase


from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            active=True,
            published_date="2021-01-01",
        )

    def test_book_list(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Book")

    def test_book_detail(self):
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["author"], "Test Author")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2021-01-01",
            "isbn": "9780743273565",
            "active": True,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["author"], "New Author")

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_date": "2021-01-01",
            "isbn": "12345678",
            "active": True,
        }
        response = self.client.put(f"/api/books/{self.book.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")
        self.assertEqual(response.data["author"], "Updated Author")
        self.assertEqual(response.data["isbn"], "12345678")

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.get(id=self.book.id).active)

    def test_free_book(self):
        response = self.client.get(f"/api/books/free/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Book")
