from api.models import LibUser
from api.serializers import UserSerializer


from django.http import HttpRequest
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


class UsersView(APIView):
    def get(self, _, id: int = None) -> Response:
        if id:
            try:
                user = LibUser.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except LibUser.DoesNotExist:
                raise NotFound(detail="User not found")
        else:
            users = LibUser.objects.filter(active=True)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        data = request.data
        data.pop("active", None)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, id: int) -> Response:
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = LibUser.objects.get(id=id)
            if not user.active:
                raise PermissionDenied(detail="User in not active")
            data = request.data
            data.pop("active", None)
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LibUser.DoesNotExist:
            raise NotFound(detail="User not found")

    def delete(self, _, id: int) -> Response:
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = LibUser.objects.get(id=id)
            if not user.active:
                raise PermissionDenied(detail="User in not active")
            user.active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LibUser.DoesNotExist:
            raise NotFound(detail="User not found")
