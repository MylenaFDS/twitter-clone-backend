from django.urls import path
from .views import RegisterView, UserMeView, UserPublicProfileView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("me/", UserMeView.as_view()),
    path("profiles/<int:pk>/", UserPublicProfileView.as_view()),  # 👈 ESSENCIAL
]


