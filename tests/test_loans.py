from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Loan, Book, LibUser


class loanAPITests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            active=True,
            isbn="123123123",
            published_date="2021-01-01",
        )
        self.user = LibUser.objects.create(
            email="test@user.com", name="test user", active=True
        )

        self.loan = Loan.objects.create(
            user=self.user, book=self.book, from_date="2021-09-01", to_date=None
        )

    def test_loan_list(self):
        response = self.client.get("/api/loans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_loan_detail(self):
        response = self.client.get(f"/api/loans/{self.loan.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "test@user.com")
        self.assertEqual(response.data["book"]["title"], "Test Book")

    def test_create_loan(self):
        new_book = Book.objects.create(
            title="New Book",
            author="New Author",
            active=True,
            isbn="1111111",
            published_date="2021-01-01",
        )

        data = {
            "book": new_book.id,
            "user": self.user.id,
            "from_date": "2021-09-01",
            "to_date": None,
        }
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["book"], new_book.id)
        self.assertEqual(Loan.objects.count(), 2)

        response = self.client.get(f"/api/books/{new_book.id}/")
        self.assertEqual(response.headers["x-user-id"], str(self.user.id))

    def test_repeated_loan(self):
        new_book = Book.objects.create(
            title="New Book",
            author="New Author",
            active=True,
            isbn="1111111",
            published_date="2021-01-01",
        )

        data = {
            "book": new_book.id,
            "user": self.user.id,
            "from_date": "2021-09-01",
            "to_date": None,
        }
        response = self.client.post("/api/loans/", data, format="json")
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Book is already borrowed"})

    def test_update_loan(self):
        response = self.client.put(f"/api/loans/{self.loan.id}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_loan(self):
        response = self.client.delete(f"/api/loans/{self.loan.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
