# accounts/models.py
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    bio = models.TextField(blank=True)


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"{self.user.username}"

