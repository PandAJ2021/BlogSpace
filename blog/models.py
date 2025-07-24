from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_identifier = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_identifier}"
        return super().save(*args, **kwargs)
    
    @property
    def likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} comment on {self.post}'
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    @property
    def likes_count(self):
        return self.likes.count()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_ikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)