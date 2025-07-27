from django.contrib import admin
from .models import Follow, Subscribe


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('author', 'follower', 'created_at',)
    search_fields = ('author',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    list_display = ('author', 'subscriber', 'created_at', 'updated_at', 'expired_at', 'is_active',)
    search_fields = ('author',)
    list_filter = ('duration',)