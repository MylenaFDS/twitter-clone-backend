from django.urls import path
from .views import Register, Login, FeedView, PostListCreate, PostRetrieveDestroy, LikeToggle, CommentListCreate, ProfileView, FollowToggle

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/<str:username>/', ProfileView.as_view()),
    path('follow/<str:username>/', FollowToggle.as_view()),
    path('feed/', FeedView.as_view()),
    path('posts/', PostListCreate.as_view()),
    path('posts/<int:pk>/', PostRetrieveDestroy.as_view()),
    path('posts/<int:post_id>/like/', LikeToggle.as_view()),
    path('posts/<int:post_id>/comments/', CommentListCreate.as_view()),
]
