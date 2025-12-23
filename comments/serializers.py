from rest_framework import serializers
from .models import Comment
from posts.serializers import UserMiniSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "post",
            "content",
            "created_at",
        ]
        read_only_fields = ["author", "created_at"]
