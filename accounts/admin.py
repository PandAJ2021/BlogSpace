from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPCode, UserProfile
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ('username',)
    list_display = ('phone', 'email', 'username', 'is_admin', 'is_active',)
    list_filter = ('is_active', 'is_admin',)
    search_fields = ('phone', 'email', 'username',)
    filter_horizontal = ()

    fieldsets = (
        ('Login Info', {'fields':('phone', 'password',)}),
        ('Personal Info', {'fields':('email', 'username',)}),
        ('Permissions', {'fields':('is_active', 'is_admin',)}),
    )

    add_fieldsets = (
        (None, {'fields':('phone', 'email', 'username', 'password', 'is_admin', 'is_active')}),
        )
    

class OTPCodeAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('phone', 'code', 'created_at', 'is_expired',)
    search_fields = ('phone',)


class UserProfileAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('user', 'name', 'surname',)
    search_fields = ('name', 'surname')


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)