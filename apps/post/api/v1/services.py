from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Count, Q, Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.post.models import Post, Reaction, Rate
from apps.post.models.reactions import ReactionStatusChoices


def create_post(user: User, post_data: dict[str, str]) -> Post:
    return Post.objects.select_related("user").create(user=user, **post_data)


def add_reaction_to_post(post_id: int, user: User, reaction_type: str) -> Reaction:
    post = get_object_or_404(Post, id=post_id)
    reaction, created = Reaction.objects.get_or_create(
        user=user,
        post=post,
        defaults={"reaction": reaction_type}
    )
    if not created:
        reaction.reaction = reaction_type
        reaction.save()
    return reaction


def add_rate_to_post(post_id: int, user: User, rate_data: dict) -> Reaction:
    post = get_object_or_404(Post, id=post_id)
    try:
        rate = Rate.objects.create(
            user=user,
            post=post,
            rate=rate_data["rate"]
        )
        return rate
    except IntegrityError:
        raise serializers.ValidationError("Already rate to this post")


def get_posts_list(filter_type: str = None) -> list:
    cache_key = f"posts_{filter_type}" if filter_type else "all_posts"
    cached_posts = cache.get(cache_key)

    if cached_posts:
        return cached_posts

    queryset = Post.objects.annotate(
        average_rating=Avg("rates__rate"),
        likes=Count("reactions", filter=Q(reactions__reaction=ReactionStatusChoices.LIKE)),
        dislikes=Count("reactions", filter=Q(reactions__reaction=ReactionStatusChoices.DISLIKE)),
    ).select_related("user").prefetch_related("reactions", "rates")

    if filter_type == "top_like":
        queryset = queryset.order_by("-likes")[:5]
    elif filter_type == "top_dislike":
        queryset = queryset.order_by("-dislikes")[:5]
    elif filter_type == "top_rate":
        queryset = queryset.order_by("-average_rating")
    elif filter_type == "min_rate":
        queryset = queryset.order_by("average_rating")

    posts = list(queryset)

    # Cache for 15 minutes
    cache.set(cache_key, posts, 60 * 15)
    return posts


def get_post_detail(post_id: int) -> Post:
    try:
        post = Post.objects.annotate(
            average_rating=Avg("rates__rate"),
            likes=Count("reactions", filter=Q(reactions__reaction=ReactionStatusChoices.LIKE)),
            dislikes=Count("reactions", filter=Q(reactions__reaction=ReactionStatusChoices.DISLIKE)),
        ).select_related("user").prefetch_related("reactions", "rates").get(id=post_id)
        return post
    except Post.DoesNotExist:
        raise serializers.ValidationError("Post not found")
