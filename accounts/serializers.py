from rest_framework import serializers
from .models import User
from follows.models import Follow


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserMeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    username = serializers.CharField(required=False)

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "banner",
            "followers_count",
            "following_count",
            "is_following",
        ]
        read_only_fields = ["id", "email"]

    def validate_username(self, value):
        user = self.instance
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError(
                "Este nome de usuário já está em uso"
            )
        return value

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        # 🔒 não seguir a si mesmo
        if request.user == obj:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()

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
