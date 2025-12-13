from django.urls import path
from .views import follow_list

urlpatterns = [
    path("", follow_list),
]
