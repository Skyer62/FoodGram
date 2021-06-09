from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from sorl.thumbnail import ImageField


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=256)
    unit = models.CharField('Единицы измерения', max_length=64)

    def __str__(self) -> str:
        return '{}, {}'.format(self.name, self.unit)


class Tag(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField(default='', unique=True, max_length=255)
    description = models.TextField('Описание', max_length=1000)
    cooking_time = models.IntegerField('Время приготовления(мин)')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe')
    image = models.ImageField('Картинка', upload_to='./media/')
    tag = models.ManyToManyField(Tag, max_length=64)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    value = models.FloatField()

    def __str__(self) -> str:
        return '{}, {}, {}'.format(self.recipe, self.ingredient, self.value)


# class TagRecipe(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

#     def __str__(self) -> str:
#         return '{}, {}'.format(self.recipe, self.tag)
