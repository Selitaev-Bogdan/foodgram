from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    """Позволяет добавлять ингредиенты прямо на странице рецепта."""

    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Конфигурация админки для рецептов."""

    list_display = ('name', 'author', 'favorite_count')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username', 'author__email')
    inlines = (RecipeIngredientInline,)

    @admin.display(description='Добавлений в избранное')
    def favorite_count(self, obj):
        """Отображает общее число добавлений рецепта в избранное."""
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Конфигурация админки для ингредиентов."""

    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Конфигурация админки для тегов."""

    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Связующая таблица ингредиентов и рецептов."""

    list_display = ('recipe', 'ingredient', 'amount')
