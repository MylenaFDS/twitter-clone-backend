from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from likes.models import Like 
from .serializers import PostSerializer
from follows.models import Follow
from comments.models import Comment


class FeedView(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(
            follower=user
        ).values_list("following_id", flat=True)

        return Post.objects.filter(author__id__in=following).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeToggleView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user, post=post
        )
        if not created:
            like.delete()
        return Response({"liked": created})
