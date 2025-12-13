from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/follows/', include('follows.urls')),
    path('api/likes/', include('likes.urls')),
    path('api/comments/', include('comments.urls')),

    # Página simples
    path('', lambda request: HttpResponse("Hello,world!")),
]
