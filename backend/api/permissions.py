from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне объекта.
    Позволяет изменять или удалять объект только его автору.
    Для всех остальных пользователей разрешено только чтение.
    """

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне конкретного объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
