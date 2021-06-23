from .models import Tag


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                f'valueIngredient_{_[1]}']
            )
    return ingredients


def get_tags(post):
    tags = {
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'dinner': 'Ужин'
    }
    tags = []
    for key, name in post.items():
        if key in tags and name == 'on':
            tags.append(Tag.objects.get(title=tags[key]))
    return tags
