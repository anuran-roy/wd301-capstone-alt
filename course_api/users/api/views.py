from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import TokenBlacklistResponseSerializer, TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer, TokenVerifyResponseSerializer, UserSerializer

# Simple JWT Views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        obj = serializer.save()
        obj.is_active = True
        obj.set_password(password)
        obj.save()

    def get_queryset(self, *args, **kwargs):
        if(self.action == "create"):
            return self.queryset
        # if(self.request.user.is_anonymous):
        #     raise PermissionError("You must be authenticated to use this API.")
        # assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        print(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Simple JWT Views
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        # Change Description
        operation_description="Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. The Access Token is valid for 5 minutes and the Refresh Token is valid for one day.",
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        # Change Description
        operation_description="Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. The Access Token is valid for 5 minutes.",
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Unused JWT Views
class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
