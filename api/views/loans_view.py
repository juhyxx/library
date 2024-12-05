from api.models import Book, Loan
from api.serializers import LoanSerializer


from rest_framework.response import Response
from rest_framework.views import APIView


class LoansView(APIView):
    def get(self, _) -> Response:
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        data = request.data
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request, id: int) -> Response:
        loan = Loan.objects.get(id=id)
        serializer = LoanSerializer(instance=loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)