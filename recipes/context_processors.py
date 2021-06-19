from .models import ShoppingList


def counter(request):
    if request.user.is_authenticated:
        count = ShoppingList.objects.filter(user=request.user).count()
    else:
        count = None
    return {'count': count}


def tags_url(request):
    tags = ''
    for item in request.GET.getlist('tags'):
        tags += f'&tags={item}'
    return {'tags': tags}
