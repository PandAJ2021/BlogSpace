from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register(r'follow', views.FollowView, basename='follow')
router.register(r'subscribe', views.SubscribeListCreateView, basename='subscribe')
router.register(r'subscribe/update', views.SubscribeUpdateView, basename='subscribe_update')

app_name = 'relationships'
urlpatterns = []
urlpatterns += router.urls