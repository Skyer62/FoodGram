from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from foodgram import settings

from recipes.forms import RecipeForm
from recipes.utils import get_ingredients, get_tags

from .models import (Ingredient, IngredientRecipe, Recipe, ShoppingList,
                     Subscription, Tag, User)


def index(request):
    recipes = Recipe.objects.all()
    tags = request.GET.getlist('tags')
    if tags:
        recipes = recipes.filter(tag__slug__in=tags).distinct().all()
    paginator = Paginator(recipes, settings.POSTS__PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Tag.objects.all()
    return render(request, 'index.html',
                  {'page': page,
                   'paginator': paginator,
                   'all_tags': all_tags})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    ingredients = IngredientRecipe.objects.filter(recipe=recipe)
    return render(request, 'singleCard.html', {'recipe': recipe,
                                               'ingredients': ingredients})


class RecipeCreateChange(View):
    def get(self, request, recipe_id=None, username=None):
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            form = RecipeForm(instance=recipe)
            title = 'Редактирование рецепта'
            bottom = 'Сохранить'
            context = {
                'form': form,
                'bottom': bottom,
                'title': title,
                'recipe': recipe,
            }
        else:
            form = RecipeForm()
            title = 'Создание рецепта'
            bottom = 'Создать рецепт'
            context = {
                'form': form,
                'bottom': bottom,
                'title': title
            }
        template = 'createChangeRecipe.html'
        return render(request, template, context)

    def post(self, request, recipe_id=None, username=None):
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            recipe.tag.set('')
            if request.user != recipe.author:
                return redirect('index')
            form = RecipeForm(request.POST or None,
                              files=request.FILES or None,
                              instance=recipe)

            context = {
                'form': form,
                'title': 'Редактирование рецепта',
                'bottom': 'Сохранить',
                'recipe': recipe
            }

        else:
            form = RecipeForm(request.POST or None,
                              files=request.FILES or None)
            context = {
                'form': form,
                'title': 'Создание рецепта',
                'bottom': 'Создать рецепт'
            }
            recipe = form.save(commit=False)

        ingredients = get_ingredients(request)
        tags = get_tags(request.POST)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif not tags:
            form.add_error(None, 'Добавьте теги')
        elif form.is_valid():
            recipe.author = request.user
            recipe.save()
            for tag in tags:
                recipe.tag.add(tag)
            recipe.save()
            IngredientRecipe.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            for title, value in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                ing_recipe = IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    value=value,
                )
                ing_recipe.save()
            form.save_m2m()

            return redirect('index')
        else:
            form = RecipeForm()
        return render(request, 'createChangeRecipe.html',
                      context=context)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def follow_index(request):
    subscriptions = Subscription.objects.filter(user=request.user).all()
    paginator = Paginator(subscriptions, settings.POSTS__PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html',
                  {'page': page,
                   'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)
    tags = request.GET.getlist('tags')
    if tags:
        recipes = recipes.filter(tag__slug__in=tags).distinct().all()
    paginator = Paginator(recipes, settings.POSTS__PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Tag.objects.all()
    recipe = page[0]
    return render(request, 'profile.html',
                  {'page': page,
                   'paginator': paginator,
                   'recipe': recipe,
                   'all_tags': all_tags})


@login_required
def favorites(request):
    recipes = Recipe.objects.filter(follow_recipe__user=request.user).all()
    tags = request.GET.getlist('tags')
    if tags:
        recipes = recipes.filter(tag__slug__in=tags).distinct().all()
    paginator = Paginator(recipes, settings.POSTS__PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Tag.objects.all()
    return render(request, 'favorite.html',
                  {'page': page,
                   'paginator': paginator,
                   'all_tags': all_tags})


@login_required
def shoplist(request):
    shoplist = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopList.html',
                  {'shoplist': shoplist})


@login_required
def shoplist_download(request):
    recipes = Recipe.objects.filter(recipe_sl__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(total_value=Sum('ingredients_recipe__value'))
    data = ''

    for item in ingredients:
        line = ' '.join(str(value) for value in item.values())
        data += line + '\n'

    response = HttpResponse(
        data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Shop List.txt"'
    return response


def about_author(request):
    return render(request, 'about_author.html')


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
