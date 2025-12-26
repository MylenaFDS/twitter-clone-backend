from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()

class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"error": "Você não pode seguir a si mesmo"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()
            return Response({"following": False})

        return Response({"following": True})


