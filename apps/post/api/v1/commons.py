from django.contrib.auth.models import User
from rest_framework import serializers

from apps.post.models import Post


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class CreatePostOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "user")


class PostOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "user", "average_rating", "likes", "dislikes")
