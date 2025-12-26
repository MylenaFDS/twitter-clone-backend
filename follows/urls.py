from django.urls import path
from .views import (
    FollowToggleView,
    FollowingListView,
    FollowersListView,
)

urlpatterns = [
    path("<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("<int:user_id>/following/", FollowingListView.as_view(), name="following-list"),
    path("<int:user_id>/followers/", FollowersListView.as_view(), name="followers-list"),
]

