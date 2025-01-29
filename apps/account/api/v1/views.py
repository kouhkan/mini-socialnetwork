from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.api.v1.services import register_user, login_user


class RegisterView(APIView):
    class RegisterInputSerializer(serializers.Serializer):
        username = serializers.CharField(min_length=4, max_length=128)
        email = serializers.EmailField(min_length=4, max_length=128)
        password = serializers.CharField(min_length=4, max_length=128)
        confirm_password = serializers.CharField(min_length=4, max_length=128)

        def validate(self, attrs):
            if attrs["password"] != attrs["confirm_password"]:
                raise serializers.ValidationError("Password does not match with confirm_password")
            attrs.pop("confirm_password")
            return attrs

    class RegisterOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "username", "email")

    @extend_schema(
        description="Register a new user",
        request=RegisterInputSerializer,
        responses={
            201: OpenApiResponse(RegisterOutputSerializer),
        },
        tags=["Auth"]
    )
    def post(self, request: Request):
        serializer = self.RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_user(serializer.validated_data)
        return Response(
            self.RegisterOutputSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    class LoginInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        password = serializers.CharField(max_length=150)

    class LoginOutputSerializer(serializers.Serializer):
        access = serializers.CharField(read_only=True)
        refresh = serializers.CharField(read_only=True)

    @extend_schema(
        description="Login user",
        request=LoginInputSerializer,
        responses={
            200: OpenApiResponse(LoginOutputSerializer),
        },
        tags=["Auth"]
    )
    def post(self, request: Request):
        serializer = self.LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = login_user(serializer.validated_data)
        return Response(
            self.LoginOutputSerializer(user).data,
            status=status.HTTP_200_OK
        )
