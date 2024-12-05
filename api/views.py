from rest_framework import generics
from api.models import LibUser, Book, Libload
from api.serializers import (
    UserSerializer,
    BookSerializer,
    LibloadSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.http import HttpRequest


class UserListCreateView(generics.ListCreateAPIView):
    queryset = LibUser.objects.all()
    serializer_class = UserSerializer


class BookView(APIView):
    def get(self, _, id: int = None) -> Response:
        if id:
            try:
                book = Book.objects.get(id=id)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                raise NotFound(detail="Book not found")
        else:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, id: int) -> Response:
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=id)
            serializer = BookSerializer(instance=book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")

    def delete(self, _, id: int) -> Response:
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")


class LibloadListCreateView(generics.ListCreateAPIView):
    queryset = Libload.objects.all()
    serializer_class = LibloadSerializer
