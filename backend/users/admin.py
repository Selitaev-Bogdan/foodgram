from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """Конфигурация админки для пользователей."""

    list_display = (
        'id', 'username', 'email', 
        'first_name', 'last_name', 'is_staff'
    )
    search_fields = ('username', 'email')
    list_filter = ('email', 'username')
    ordering = ('username',)
