from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r'admin', views.AdminUserViewSet)

app_name = 'accounts'
urlpatterns =[
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
] 

urlpatterns += router.urls