from rest_framework import serializers
from .models import Comment
from accounts.models import User


class CommentAuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Comment._meta.get_field("post").remote_field.model.objects.all())

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",        # 🔹 OBRIGATÓRIO
            "author",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "author", "created_at"]
