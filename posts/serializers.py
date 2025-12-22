from rest_framework import serializers
from .models import Post
from accounts.models import User


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "likes_count",
            "liked",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
