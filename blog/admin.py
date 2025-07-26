from django.contrib import admin
from .models import Post, Comment, Category, Tag, PostLike, CommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    list_display = ('author', 'title', 'category', 'is_published', 'updated_at',)
    search_fields = ('author__username', 'category__name', 'tags__name',)
    list_filter = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('post', 'user', 'is_approved',)
    search_fields = ('post_title', 'content', 'user__username',)
    list_filter = ('is_approved',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(PostLike)
admin.site.register(CommentLike)