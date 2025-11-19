from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PostViewSet, ProfileViewSet, UserViewSet, FollowToggleView, LikeToggleView, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'users', UserViewSet, basename='users')

posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow-toggle'),
    path('like/<int:post_id>/', LikeToggleView.as_view(), name='like-toggle'),
]
