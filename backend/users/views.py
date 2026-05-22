from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.recipes.models import Follow
from backend.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user

        if request.method == 'POST':
            if user == author or Follow.objects.filter(user=user,
                                                       author=author).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, author=author)
            if not follow.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
