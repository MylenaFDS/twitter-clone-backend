from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowUserSerializer

User = get_user_model()


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"error": "Você não pode seguir a si mesmo"},
                status=400
            )

        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"},
                status=404
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()
            return Response({"following": False})

        return Response({"following": True})


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        followers = Follow.objects.filter(
            following_id=user_id
        ).select_related("follower")

        users = [follow.follower for follow in followers]
        serializer = FollowUserSerializer(users, many=True)
        return Response(serializer.data)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        following = Follow.objects.filter(
            follower_id=user_id
        ).select_related("following")

        users = [follow.following for follow in following]
        serializer = FollowUserSerializer(users, many=True)
        return Response(serializer.data)



