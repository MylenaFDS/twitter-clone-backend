from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer
from follows.models import Follow
from likes.models import Like

# 🔹 CRUD padrão (router)
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        author = self.request.query_params.get("author")

        if author == "me":
            return Post.objects.filter(author=user).order_by("-created_at")

        return Post.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 🔹 Feed personalizado
class FeedView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(
            follower=user
        ).values_list("following_id", flat=True)

        return Post.objects.filter(
            author__id__in=following
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
# 🔹 Like / Unlike
class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            like.delete()

        return Response({"liked": created})
