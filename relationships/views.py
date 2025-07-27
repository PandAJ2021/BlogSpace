from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet
from .models import Follow, Subscribe
from .serializers import FollowSerializer
from rest_framework.permissions import IsAuthenticated


class FollowView(ListCreateAPIView, DestroyAPIView, GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)