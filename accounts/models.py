# accounts/models.py
import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


# =========================
# VALIDADOR DE IMAGEM
# =========================
def validate_image(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Imagem maior que 2MB")

    if image.content_type not in ["image/jpeg", "image/png"]:
        raise ValidationError("Formato inválido. Use JPG ou PNG.")


# =========================
# USER
# =========================
class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    banner = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True,
        validators=[validate_image],
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username


# =========================
# PASSWORD RESET TOKEN
# =========================
class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"{self.user.username}"
