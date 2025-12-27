from django.urls import path
from .views import RegisterView, UserMeView, UserDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", UserMeView.as_view(), name="user-me"),
    path("<int:id>/", UserDetailView.as_view()),
]

