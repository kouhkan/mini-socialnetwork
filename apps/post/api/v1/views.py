from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.api.v1.commons import PostOutputSerializer, CreatePostOutputSerializer
from apps.post.api.v1.services import create_post, add_reaction_to_post, get_posts_list, add_rate_to_post, \
    get_post_detail
from apps.post.models.reactions import ReactionStatusChoices


class SendPostView(APIView):
    permission_classes = [IsAuthenticated]

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=500)

    @extend_schema(
        description="Create a new post",
        request=PostInputSerializer,
        responses={201: OpenApiResponse(CreatePostOutputSerializer)},
        tags=["Post"]
    )
    def post(self, request: Request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = create_post(request.user, serializer.validated_data)

        return Response(
            PostOutputSerializer(post).data,
            status=status.HTTP_201_CREATED
        )


class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        description="Retrieve posts with optional filters",
        parameters=[
            OpenApiParameter(name="filter", type=str, required=False,
                             enum=["top_like", "top_dislike", "max_rate", "min_rate"])
        ],
        responses={200: PostOutputSerializer(many=True)},
        tags=["Post"]
    )
    def get(self, request: Request):
        filter_type = request.query_params.get("filter")
        posts = get_posts_list(filter_type)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostOutputSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve single post",
        responses={200: PostOutputSerializer()},
        tags=["Post"]
    )
    def get(self, request: Request, post_id: int):
        post = get_post_detail(post_id)
        return Response(
            PostOutputSerializer(post).data,
            status=status.HTTP_200_OK
        )


class ReactToPostView(APIView):
    permission_classes = [IsAuthenticated]

    class ReactionInputSerializer(serializers.Serializer):
        reaction = serializers.ChoiceField(choices=ReactionStatusChoices.choices)

    @extend_schema(
        description="Add/update reaction to a post",
        request=ReactionInputSerializer,
        responses={200: OpenApiResponse(description="Success")},
        tags=["Reaction"]
    )
    def post(self, request: Request, post_id: int):
        serializer = self.ReactionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        add_reaction_to_post(post_id, request.user, serializer.validated_data['reaction'])
        return Response({"detail": "Reaction updated"}, status=status.HTTP_200_OK)


class RateToPostView(APIView):
    permission_classes = [IsAuthenticated]

    class RateInputSerializer(serializers.Serializer):
        rate = serializers.IntegerField(min_value=1, max_value=5)

    @extend_schema(
        description="Add rate to post",
        request=RateInputSerializer,
        responses={200: OpenApiResponse(description="Success")},
        tags=["Rate"]
    )
    def post(self, request: Request, post_id: int):
        serializer = self.RateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        add_rate_to_post(post_id, request.user, serializer.validated_data)
        return Response({"detail": "Rate updated"}, status=status.HTTP_200_OK)
