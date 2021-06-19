from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.utils import json

from recipes.models import Recipe, Subscription, Ingredient, \
                                ShoppingList, Favorite


class Ingredients(LoginRequiredMixin, View):
    def get(self, request):
        text = request.GET['query']
        ingredients = list(Ingredient.objects.filter(
            title__icontains=text).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class Subscribes(LoginRequiredMixin, View):
    def post(self, request):
        author_id = json.loads(request.body)["id"]
        if author_id:
            author = get_object_or_404(User, id=author_id)
            created = Subscription.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        sub = get_object_or_404(Subscription, user=request.user, author=author)
        sub.delete()
        return JsonResponse({"success": True})


class Purchases(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body)["id"]
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            created = ShoppingList.objects.get_or_create(
                recipe=recipe, user=request.user
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = get_object_or_404(ShoppingList, user=request.user, recipe=recipe)
        purchase.delete()
        return JsonResponse({"success": True})


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body)["id"]
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            created = Favorite.objects.get_or_create(
                recipe=recipe, user=request.user
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        user = get_object_or_404(
            User, username=request.user.username
        )
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return JsonResponse({"success": True})
