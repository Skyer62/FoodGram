from django import forms
from django.contrib import admin
from .models import Ingredient, Recipe, IngredientRecipe, Tag


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, )


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Tag)
