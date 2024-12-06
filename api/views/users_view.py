from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request

from api.models import LibUser
from api.serializers import UserSerializer


class UsersView(ModelViewSet):
    queryset = LibUser.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request) -> Response:
        users = self.queryset.filter(active=True)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LibUser.DoesNotExist:
            raise NotFound(detail="User not found")

    def create(self, request: Request) -> Response:
        data = request.data
        data.pop("active", None)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk: int = None) -> Response:
        user = self.get_object()
        if not user.active:
            raise PermissionDenied(detail="User is not active")
        data = request.data
        data.pop("active", None)
        serializer = self.get_serializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: int = None) -> Response:
        user = self.get_object()
        if not user.active:
            raise PermissionDenied(detail="User is not active")
        user.active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
