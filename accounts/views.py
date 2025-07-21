from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .models import User, UserProfile, SocialLink
from .serializers import UserRegisterSerializer, AdminUserSerializer, UserProfileSerializer, SocialLinkSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = AdminUserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class UserLogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)

            if token.payload['user_id'] != request.user.id:
                return Response(data={'detail':'Token does not belongs to authentication user'},
                                status=status.HTTP_403_FORBIDDEN)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError as err:
            return Response(data={'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(data={'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)


class SocialLinkViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListProfileView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileView(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    @action(detail=False, methods=['get',], url_path='me')
    def me(self, request):
        profile = self.get_object()
        ser_data = self.get_serializer(profile)
        return Response(ser_data.data)