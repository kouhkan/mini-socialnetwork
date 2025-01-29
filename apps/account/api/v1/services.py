from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


def register_user(user_data: dict[str, str]) -> User:
    try:
        return User.objects.create_user(**user_data)
    except IntegrityError:
        raise serializers.ValidationError("User already exists.")


def login_user(user_data: dict[str, str]) -> dict:
    if not (user := authenticate(**user_data)):
        raise serializers.ValidationError("Login credentials is not valid")

    refresh_token = RefreshToken.for_user(user)
    return {
        "access": str(refresh_token.access_token),
        "refresh": str(refresh_token),
    }
