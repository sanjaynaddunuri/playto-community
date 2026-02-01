from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, leaderboard_view, like_view

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("leaderboard/", leaderboard_view),
    path("like/", like_view),
]

urlpatterns += router.urls
