from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserRegisterSerializer, AdminUserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = AdminUserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

