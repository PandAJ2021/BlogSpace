from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Post, Comment, Category, Tag
from .serializers import PublicPostSerializer, UserPostSerilaizer
from rest_framework.permissions import IsAuthenticated


class ListRetrievePostView(ListAPIView, RetrieveAPIView, GenericViewSet):
    serializer_class = PublicPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class UserPostView(ModelViewSet):
    serializer_class = UserPostSerilaizer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)