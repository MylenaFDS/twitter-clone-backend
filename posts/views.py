from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import Post, Like
from .serializers import PostSerializer
from follows.models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()


# 🔹 CRUD padrão (timeline própria / curtidos / etc)
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        author = self.request.query_params.get("author")
        liked = self.request.query_params.get("liked")

        queryset = Post.objects.all()

        # 🧾 Tweets do próprio usuário
        if author == "me":
            queryset = queryset.filter(author=user)

        # 🧾 Tweets de um usuário específico (author=id)
        elif author and author.isdigit():
            queryset = queryset.filter(author_id=author)

        # ❤️ Tweets curtidos pelo usuário
        if liked == "me":
            queryset = queryset.filter(
                likes__user=user
            ).distinct()

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# 🔹 Feed personalizado (seguindo + eu)
class FeedView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user

        following_ids = Follow.objects.filter(
            follower=user
        ).values_list("following_id", flat=True)

        return Post.objects.filter(
            author__in=[*following_ids, user.id]
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# ✅ Posts de um usuário específico (perfil)
class UserPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)

        return Post.objects.filter(
            author=user
        ).order_by("-created_at")

    def get_serializer_context(self):
        return {"request": self.request}


# 🔹 Like / Unlike
class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            like.delete()

        return Response({"liked": created})

