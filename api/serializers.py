from rest_framework import serializers
from .models import LibUser, Book, Libload


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUser
        fields = ["id", "username", "email"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = "books"
        model = Book
        fields = ["id", "title", "author", "published_date", "isbn"]


class LibloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libload
        fields = ["id", "user", "book", "borrowed_date", "return_date"]
