from rest_framework import serializers
from .models import LibUser, Book, Loan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUser
        fields = ["id", "name", "email", "active"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = "books"
        model = Book
        fields = ["id", "title", "author", "published_date", "isbn", "active"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "user", "book", "borrowed_date", "return_date"]
