from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'posts', views.ListRetrievePostView, basename='posts')
router.register(r'my-posts', views.UserPostView, basename='my_posts')

app_name = 'blog'
urlpatterns = []
urlpatterns += router.urls