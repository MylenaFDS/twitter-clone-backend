from django.urls import path
from .views import FeedView, LikeToggleView

urlpatterns = [
    # Feed de posts (GET = listar, POST = criar)
    path('', FeedView.as_view(), name='feed'),

    # Curtir / descurtir post
    path('<int:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
]

