from django.urls import path
from .views import (
    RegisterView,
    UserMeView,
    UserPublicProfileView,
    UserFollowersView,
    UserFollowingView,
    UnfollowUserView,
    UserSuggestionsView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("me/", UserMeView.as_view()),
    path("profiles/<int:pk>/", UserPublicProfileView.as_view()),

    path("users/<int:id>/followers/", UserFollowersView.as_view()),
    path("users/<int:id>/following/", UserFollowingView.as_view()),

    # 🔴 NOVAS ROTAS
    path("users/<int:id>/unfollow/", UnfollowUserView.as_view()),
    path("users/suggestions/", UserSuggestionsView.as_view()),

    
    # 🔐 RESET DE SENHA
    path("password-reset/request/", PasswordResetRequestView.as_view()),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view()),
]
