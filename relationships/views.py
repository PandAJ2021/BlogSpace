from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import GenericViewSet
from .models import Follow, Subscribe
from .serializers import FollowSerializer, SubscribeUpdateSerializer ,SubscribeCreateSerializer
from rest_framework.permissions import IsAuthenticated


class FollowView(ListCreateAPIView, DestroyAPIView, GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


class SubscribeListCreateView(ListCreateAPIView, GenericViewSet):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def get_queryset(self):
        return Subscribe.objects.filter(subscriber=self.request.user)


class SubscribeUpdateView(UpdateAPIView, GenericViewSet):
    serializer_class = SubscribeUpdateSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def get_queryset(self):
        return Subscribe.objects.filter(subscriber=self.request.user)