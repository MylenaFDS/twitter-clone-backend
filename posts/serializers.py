from rest_framework import serializers
from .models import Post
from accounts.models import User
from comments.models import Comment


# =========================
# SERIALIZER DO AUTOR (COM AVATAR E BANNER)
# =========================
class PostAuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "avatar", "banner"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_banner(self, obj):
        request = self.context.get("request")
        if obj.banner and request:
            return request.build_absolute_uri(obj.banner.url)
        return None


# =========================
# COMENTÁRIOS
# =========================
class CommentSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "content",
            "created_at",
        ]


# =========================
# POSTS
# =========================
class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "likes_count",
            "liked",
            "comments_count",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments_count(self, obj):
        return obj.comments.count()
