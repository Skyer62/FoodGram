from django import template

from recipes.models import Favorite, ShoppingList, Subscription

register = template.Library()


@register.filter(name='is_subscribe')
def is_subscribe(author, user):
    return Subscription.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_purchase')
def is_purchase(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()
