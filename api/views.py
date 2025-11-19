from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, Post, Follow, Like, Comment
from .serializers import (ProfileSerializer, PostSerializer, FollowSerializer, 
                          LikeSerializer, CommentSerializer, UserSerializer)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # IDs dos usuários que o user segue
        following_ids = user.following.values_list('followed_id', flat=True)
        # feed com posts de seguidos + próprios
        return Post.objects.filter(author__id__in=list(following_ids) + [user.id]).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'put'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class FollowToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        try:
            followed = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        follow, created = Follow.objects.get_or_create(follower=follower, followed=followed)
        if not created:
            follow.delete()
            return Response({"detail": "Unfollowed"})
        return Response({"detail": "Followed"})

class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return Response({"detail": "Unliked"})
        return Response({"detail": "Liked"})

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post__id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = generics.get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create your views here.
