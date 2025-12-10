from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Follow, Like, Profile
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly

class Register(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'username and password required'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'username taken'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class Login(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Credenciais inválidas'}, status=400)

class ProfileView(APIView):
    def get(self, request, username=None):
        user = request.user if username is None else get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data)
    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        data = request.data
        profile.bio = data.get('bio', profile.bio)
        profile.avatar = data.get('avatar', profile.avatar)
        profile.save()
        if data.get('password'):
            request.user.set_password(data['password'])
            request.user.save()
        return Response(ProfileSerializer(profile).data)

class FollowToggle(APIView):
    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return Response({'error':'cannot follow yourself'}, status=400)
        rel = Follow.objects.filter(follower=request.user, followed=target).first()
        if rel:
            rel.delete()
            return Response({'status':'unfollowed'})
        Follow.objects.create(follower=request.user, followed=target)
        return Response({'status':'followed'})

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = Follow.objects.filter(follower=user).values_list('followed', flat=True)
        return Post.objects.filter(author__in=following_ids).order_by('-created_at')

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class LikeToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'status':'unliked'})
        Like.objects.create(user=request.user, post=post)
        return Response({'status':'liked'})

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user, post=post)
