from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse

from users.views import UserViewSet
from posts.views import PostViewSet, FeedView
from follows.views import FollowViewSet
from likes.views import LikeViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"follows", FollowViewSet, basename="follows")
router.register(r"likes", LikeViewSet, basename="likes")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📰 Feed personalizado
    path("api/feed/", FeedView.as_view(), name="feed"),

    # 🌐 API padrão
    path("api/", include(router.urls)),

    path("", lambda request: HttpResponse("Hello, world!")),
]
