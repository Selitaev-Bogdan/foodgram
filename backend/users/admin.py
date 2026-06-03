from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff'
    )
    list_display_links = ('username', 'email')
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)
