from django.urls import path
from .views import like_list

urlpatterns = [
    path("", like_list),
]
