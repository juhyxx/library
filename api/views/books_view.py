from collections import defaultdict
from typing import Any, Dict, List

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Book, Loan, LibUser
from api.serializers import (
    BookSerializer,
    LoanSerializer,
    UserSerializer,
    SimpleBookSerializer,
)


class BooksView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self) -> Any:
        return super().get_queryset().filter(active=True)

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        if not instance.active:
            raise PermissionDenied(detail="Book is not active")

        result_data = self.get_serializer(instance).data
        headers = {}

        loan = Loan.objects.filter(book=instance, to_date=None).first()
        if loan:
            loan_data = LoanSerializer(loan).data

            headers["x-user-id"] = loan_data.pop("user", None)
            result_data["from_date"] = loan_data.get("from_date")

        return Response(result_data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data
        data.pop("active", None)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        if not instance.active:
            raise PermissionDenied(detail="Book is not active")

        data = request.data
        data.pop("active", None)
        serializer = self.get_serializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        if not instance.active:
            raise PermissionDenied(detail="Book is not active")

        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def free(self, request) -> Response:
        loans = Loan.objects.filter(to_date=None)
        books = self.queryset.filter(active=True).exclude(loan__in=loans)
        book_data = SimpleBookSerializer(books, many=True).data

        return Response(book_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def borrowed(self, request) -> Response:
        loans = Loan.objects.filter(to_date=None).order_by("user")
        user_loans = defaultdict(list)

        for loan in loans:
            user_loans[loan.user].append(loan)

        result = []

        for user, loans_list in user_loans.items():
            user_data = UserSerializer(user).data
            books_data = []
            for loan in loans_list:
                book_data = SimpleBookSerializer(loan.book).data
                book_data["from_date"] = loan.from_date
                books_data.append(book_data)

            user_data["books"] = books_data
            result.append(user_data)

        return Response(result, status=status.HTTP_200_OK)
