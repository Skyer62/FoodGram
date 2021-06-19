from api.views import Favorite, Ingredient
from django import forms
from django.contrib import admin
from .models import Ingredient, Recipe, IngredientRecipe, \
    ShoppingList, Tag, Subscription, Favorite


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('title', 'author')
    inlines = (IngredientRecipeInLine, )


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe')
    list_filter = ('ingredient', 'recipe')


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')
    fields = ('author', 'user')


admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ShoppingList, ShopListAdmin)
admin.site.register(Favorite, FavoritesAdmin)
