from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from users.views import UserViewSet
from posts.views import PostViewSet, FeedView, LikeToggleView
from comments.views import CommentViewSet
from accounts.views import RegisterView, UserMeView, ChangePasswordView

# 🔹 Router padrão (CRUD)
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 🧾 Registro / usuário logado
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/me/", UserMeView.as_view(), name="user-me"),
    path(
        "api/change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),

    # 📰 Feed (somente posts de pessoas seguidas)
    path(
        "api/posts/feed/",
        FeedView.as_view(),
        name="feed",
    ),

    # ❤️ Like / Unlike
    path(
        "api/posts/<int:post_id>/like/",
        LikeToggleView.as_view(),
        name="post-like-toggle",
    ),

    # 👥 Seguir / deixar de seguir
    path("api/follows/", include("follows.urls")),

    # 🌐 API padrão (CRUD)
    path("api/", include(router.urls)),

    path("", lambda request: HttpResponse("Hello, world!")),
]

# 🖼️ MEDIA FILES (avatar / banner) — somente em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
