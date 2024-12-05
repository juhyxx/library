from collections import defaultdict
from api.models import Book, Loan
from api.serializers import LoanSerializer, UserSerializer
from api.serializers import BookSerializer
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


@api_view(['GET'])
def free(_):
    loans = Loan.objects.filter(return_date=None)
    books = Book.objects.filter(active=True).exclude(loan__in=loans)
    book_data = BookSerializer(books, many=True).data
    for book in book_data:
        book.pop("active", None)
    return Response(book_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def borrowed(_):
    loans = Loan.objects.filter(return_date=None).order_by('user')
    user_books = defaultdict(list)
    
    for loan in loans:
        user_books[loan.user].append(loan.book)
    
    result = []
    
    for user, books in user_books.items():
        user_data = UserSerializer(user).data
        user_data['books'] = BookSerializer(books, many=True).data
        result.append(user_data)

    return Response(result, status=status.HTTP_200_OK)