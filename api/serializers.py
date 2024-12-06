from rest_framework import serializers
from api.models import LibUser, Book, Loan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibUser
        fields = ["id", "name", "email", "active"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = "books"
        model = Book
        fields = ["id", "title", "author", "published_date", "isbn", "active"]


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = "books"
        model = Book
        fields = ["id", "title", "author"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "user", "book", "from_date", "to_date"]


class CombinedLoanSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookSerializer()

    class Meta:
        model = Loan
        fields = ["id", "user", "book", "from_date", "to_date"]
