from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'posts', views.ReadOnlyPostView, basename='posts')
router.register(r'my-posts', views.UserPostView, basename='my_posts')
router.register(r'my-comments', views.UserCommentView, basename='my-comments')

app_name = 'blog'
urlpatterns = [
    path('post/comments/', views.ListCommentsView.as_view(), name='post_comments'),
    path('post/like/<slug:post_slug>/', views.PostLikeView.as_view(), name='post_like'),
    path('post/comment/like/<int:comment_id>/', views.CommentLikeView.as_view(), name='comment_like'),

]
urlpatterns += router.urls