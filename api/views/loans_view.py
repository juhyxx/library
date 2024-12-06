from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.request import Request

from api.models import Book, Loan
from api.serializers import LoanSerializer, CombinedLoanSerializer


class LoansView(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def list(self, request: Request) -> Response:
        loans = self.queryset.order_by("from_date")
        serializer = CombinedLoanSerializer(loans, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        serializer = CombinedLoanSerializer(self.get_object())
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        data = request.data
        serializer = self.get_serializer(data=data)

        book = Book.objects.filter(active=True, id=data["book"]).first()

        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if self.queryset.filter(book=book, to_date=None).exists():
            return Response(
                {"error": "Book is already borrowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=["get"])
    def return_book(self, request: Request, pk: int) -> Response:
        loan = self.get_object()
        loan.return_book()

        return Response(status=status.HTTP_204_NO_CONTENT)
