from api.models import Book
from api.serializers import BookSerializer


from django.http import HttpRequest
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


class BooksView(APIView):
    def get(self, _, id: int = None) -> Response:
        if id:
            try:
                book = Book.objects.get(id=id)
                if not book.active:
                    raise PermissionDenied(detail="Book in not active")
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                raise NotFound(detail="Book not found")
        else:
            books = Book.objects.filter(active=True)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        data = request.data
        data.pop("active", None)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, id: int) -> Response:
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=id)
            if not book.active:
                raise PermissionDenied(detail="Book in not active")
            data = request.data
            data.pop("active", None)
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
            if not book.active:
                raise PermissionDenied(detail="Book in not active")
            book.active = False
            book.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")
