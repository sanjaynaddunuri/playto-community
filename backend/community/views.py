from datetime import timedelta

from django.db import transaction, IntegrityError
from django.db.models import Sum, Case, When, IntegerField
from django.utils.timezone import now

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment, Like
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(["POST"])
def like_view(request):
    user_id = request.data.get("user_id")
    post_id = request.data.get("post_id")
    comment_id = request.data.get("comment_id")

    if not user_id or (not post_id and not comment_id):
        return Response(
            {"error": "user_id and post_id OR comment_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            Like.objects.create(
                user_id=user_id,
                post_id=post_id,
                comment_id=comment_id
            )
            return Response({"message": "liked"}, status=201)

    except IntegrityError:
        return Response({"error": "already liked"}, status=409)

@api_view(["GET"])
def leaderboard_view(request):
    last_24h = now() - timedelta(hours=24)

    data = (
        Like.objects
        .filter(created_at__gte=last_24h)
        .annotate(
            karma=Case(
                When(post__isnull=False, then=5),
                When(comment__isnull=False, then=1),
                output_field=IntegerField()
            )
        )
        .values("user__username")
        .annotate(total_karma=Sum("karma"))
        .order_by("-total_karma")[:5]
    )

    return Response(list(data))
