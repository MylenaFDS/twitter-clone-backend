from django.urls import path
from .views import FeedView, LikeToggleView, UserPostsView

urlpatterns = [
    # 📰 Feed (seguindo + eu)
    path("feed/", FeedView.as_view(), name="feed"),

    # 👤 Posts de um usuário (perfil)
    path(
        "users/<int:user_id>/posts/",
        UserPostsView.as_view(),
        name="user-posts"
    ),

    # ❤️ Curtir / descurtir post
    path(
        "<int:post_id>/like/",
        LikeToggleView.as_view(),
        name="like-toggle"
    ),
]

