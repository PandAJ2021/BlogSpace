from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r'admin', views.AdminUserViewSet, basename='admin')
router.register(r'profiles', views.ListRetrieveProfileView, basename='profiles')
router.register(r'profile', views.UserProfileView, basename='profile')
router.register(r'social-links', views.SocialLinkViewSet, basename='social-link')

app_name = 'accounts'
urlpatterns =[
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('auth/send-otp/', views.SendOTPView.as_view(), name='send_otp_code'),
    path('auth/token-by-otp/', views.OTPLoginView.as_view(), name='token_by_otp'),
] 

urlpatterns += router.urls