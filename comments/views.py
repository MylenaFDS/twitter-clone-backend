from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthor

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        queryset = Comment.objects.select_related("author")

        post_id = self.request.query_params.get("post")
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset.order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
