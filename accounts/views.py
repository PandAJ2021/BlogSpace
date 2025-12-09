from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .models import User, UserProfile, SocialLink, OTPCode
from .serializers import UserRegisterSerializer, AdminUserSerializer, UserProfileSerializer, SocialLinkSerializer, OTPLoginSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
import random, re
from uttils import send_otp_code


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
        user = self.request.user

        if SocialLink.objects.filter(user=user).count() >= 10:
            raise serializers.ValidationError({'detail': 'Max 10 social links allowed.'}, code=status.HTTP_403_FORBIDDEN)
            
        serializer.save(user=user)


class ListRetrieveProfileView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
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


class SendOTPView(APIView):

    def post(self, request):
        phone = request.data.get('phone')

        if not phone or not re.fullmatch('09\d{9}', phone):
            return Response({'detail':'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(phone=phone, is_active=True).exists():
            return Response({'detail':'There is no user with this number'}, status=status.HTTP_400_BAD_REQUEST)
        
        last_otp= OTPCode.objects.filter(phone=phone).order_by('-created_at').first()
        if last_otp and not last_otp.is_expired:
            return Response({'detail':"Code sent recently, Please wait"}, status=status.HTTP_400_BAD_REQUEST)

        random_code = random.randint(100000, 999999)
        OTPCode.objects.create(phone=phone, code=random_code)
        send_otp_code(phone_number=phone, code=random_code)

        return Response({'phone':phone, 'detail':'Verification code sent'}, status=status.HTTP_200_OK)


class OTPLoginView(APIView):

    def post(self, request):

        ser_data = OTPLoginSerializer(data=request.data)
        if ser_data.is_valid():
            phone = ser_data.validated_data['phone']
            code = ser_data.validated_data['code']

            try:
                otp = OTPCode.objects.get(phone=phone, code=code)
            except OTPCode.DoesNotExist:
                return Response({'detail': 'Invalid code or phone'}, status=status.HTTP_400_BAD_REQUEST)
            if otp.is_expired:
                return Response({'detail': 'OTP is expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                return Response({'detail':'There is no user with this number'}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response(data={
                'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)