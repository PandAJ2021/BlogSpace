from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Post, Comment, PostLike, CommentLike
from .serializers import ReadOnlyPostSerializer, UserPostSerilaizer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ReadOnlyPublicPostView(ReadOnlyModelViewSet):
    serializer_class = ReadOnlyPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True, is_premium=False)


class ReadOnlyPremiumPostView(ReadOnlyModelViewSet):
    serializer_class = ReadOnlyPostSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'slug'

    def get_queryset(self):
        authors = self.request.user.subscriptions.values_list('author', flat=True)
        return Post.objects.filter(is_published=True, is_premium=True, author__in=authors)
    

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
    

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail':'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostLikeSerializer(instance=like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        like = get_object_or_404(PostLike, user=request.user, post=post)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            return Response({'detail':'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentLikeSerializer(instance=like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = get_object_or_404(CommentLike, user=request.user, comment=comment)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)