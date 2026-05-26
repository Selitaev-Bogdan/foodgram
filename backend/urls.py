from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('backend.recipes.urls')),
]
