from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Post, Comment, Category, Tag
from .serializers import PublicPostSerializer, UserPostSerilaizer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .permissions import IsOwner


class ReadOnlyPostView(ReadOnlyModelViewSet):
    serializer_class = PublicPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class UserPostView(ModelViewSet):
    serializer_class = UserPostSerilaizer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class ListCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_slug = self.request.query_params.get('post_slug')
        if not post_slug:
            raise ValidationError({'post_slug':'This query parameter is required'})
        post = get_object_or_404(Post, slug=post_slug)
        return Comment.objects.filter(post = post, is_approved=True)


class UserCommentView(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)