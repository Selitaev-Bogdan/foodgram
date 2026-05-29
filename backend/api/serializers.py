from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
    UserSerializer as DjoserUserSerializer
)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.constants import MIN_AMOUNT, MIN_COOKING_TIME
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Follow

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """Отображение информации о пользователе."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class UserCreateSerializer(DjoserUserCreateSerializer):
    """Регистрация новых пользователей."""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Упрощенный формат рецепта для списков подписок и избранного."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionsSerializer(UserSerializer):
    """Отображение авторов, на которых подписан пользователь, с их рецептами"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except (ValueError, TypeError):
                pass
        return ShortRecipeSerializer(queryset, many=True, read_only=True).data


class SubscribeSerializer(serializers.ModelSerializer):
    """Создание и валидация подписки."""
    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя.'
            )
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise ValidationError('Нельзя подписаться на самого себя.')
        return data

    def to_representation(self, instance):
        return UserSubscriptionsSerializer(
            instance.author,
            context=self.context
        ).data



class TagSerializer(serializers.ModelSerializer):
    """Работа с тегами."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Работа с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Отображение ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Чтение рецептов (GET)."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipe_ingredients'
    )
    image = Base64ImageField()
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True, default=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Создание и обновление рецептов (POST, PATCH)."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        error_messages={
            'min_value': f'Минимальное время — {MIN_COOKING_TIME} мин.'
        }
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        return RecipeIngredientSerializer(
            obj.recipe_ingredients.all(), many=True
        ).data

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError('Нужен хотя бы один ингредиент.')

        ingredient_list = []
        for item in ingredients:
            try:
                amount = int(item.get('amount'))
            except (ValueError, TypeError):
                raise ValidationError('Количество должно быть числом.')

            if amount < MIN_AMOUNT:
                raise ValidationError(f'Минимальное количество—{MIN_AMOUNT}.')

            ingredient_id = item.get('id')
            if not ingredient_id:
                raise ValidationError('У ингредиента должен быть ID.')
            if ingredient_id in ingredient_list:
                raise ValidationError('Ингредиенты не должны повторяться.')
            ingredient_list.append(ingredient_id)

        tags = self.initial_data.get('tags')
        if not tags:
            raise ValidationError('Нужен хотя бы один тег.')
        if len(set(tags)) != len(tags):
            raise ValidationError('Теги не должны повторяться.')

        return data

    def _set_ingredients_and_tags(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ])

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = self.initial_data.get('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self._set_ingredients_and_tags(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = self.initial_data.get('ingredients')
        instance = super().update(instance, validated_data)
        self._set_ingredients_and_tags(instance, tags, ingredients)
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data
