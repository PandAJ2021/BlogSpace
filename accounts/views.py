from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserRegisterSerializer, AdminUserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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