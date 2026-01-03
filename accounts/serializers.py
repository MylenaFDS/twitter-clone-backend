from rest_framework import serializers
from .models import User
from follows.models import Follow


# =========================
# REGISTER
# =========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# =========================
# USER ME
# =========================
class UserMeSerializer(serializers.ModelSerializer):
    # 🔹 campos REAIS (write)
    avatar = serializers.ImageField(required=False, allow_null=True)
    banner = serializers.ImageField(required=False, allow_null=True)

    # 🔹 campos de leitura (Cloudinary URL)
    avatar_url = serializers.SerializerMethodField(read_only=True)
    banner_url = serializers.SerializerMethodField(read_only=True)

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

            # 👇 IMPORTANTÍSSIMO
            "avatar",
            "banner",

            "avatar_url",
            "banner_url",

            "followers_count",
            "following_count",
            "is_following",
        ]
        read_only_fields = [
            "id",
            "email",
            "followers_count",
            "following_count",
            "is_following",
            "avatar_url",
            "banner_url",
        ]

    # 🔢 contadores
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    # 👥 segue?
    def get_is_following(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        if request.user == obj:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()

    # 🖼️ avatar (Cloudinary)
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    # 🖼️ banner (Cloudinary)
    def get_banner_url(self, obj):
        if obj.banner:
            return obj.banner.url
        return None


# =========================
# USER LIST
# =========================
class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "avatar", "is_following"]

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def get_is_following(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        if request.user == obj:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()
