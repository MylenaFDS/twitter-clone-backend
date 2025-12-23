from django.db import models
from django.conf import settings
from posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} comentou no post {self.post.id}"

