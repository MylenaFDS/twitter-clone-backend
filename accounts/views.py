from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)

from .serializers import UserMeSerializer

User = get_user_model()


# =========================
# REGISTRO
# =========================
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username e senha são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Usuário já existe"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return Response(
            {"message": "Usuário criado com sucesso"},
            status=status.HTTP_201_CREATED,
        )


# =========================
# MEU PERFIL (/api/me/)
# =========================
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        serializer = UserMeSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================
# PERFIL DE OUTRO USUÁRIO (/api/users/<id>/)
# =========================

class UserPublicProfileView(APIView):
    permission_classes = [AllowAny]  # 👈 ISSO É ESSENCIAL

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        serializer = UserMeSerializer(
            user,
            context={"request": request}
        )

        return Response(serializer.data)
# =========================
# ALTERAR SENHA
# =========================
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"error": "Informe a senha atual e a nova senha"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Senha atual incorreta"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Senha alterada com sucesso"},
            status=status.HTTP_200_OK,
        )
