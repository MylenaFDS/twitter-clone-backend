from django.test import TestCase
from accounts.models import User
from .models import Post

class PostTest(TestCase):
    def test_create_post(self):
        user = User.objects.create_user(username="test", password="123")
        post = Post.objects.create(author=user, content="Hello")
        self.assertEqual(post.content, "Hello")
