from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField('Название', max_length=256, null=True, blank=True)
    dimension = models.CharField(
        'Единицы измерения', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    title = models.CharField('Названание', max_length=64, unique=True)
    slug = models.SlugField('Идентификатор', unique=True,
                            max_length=100, blank=True, null=True)
    color = models.CharField('Цвет', max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='recipes')
    title = models.CharField('Название рецепта', max_length=255)
    description = models.TextField('Описание', max_length=1000)
    cooking_time = models.PositiveIntegerField(
        'Время приготовления(мин)', validators=[MinValueValidator(1)])
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe')
    image = models.ImageField('Картинка', upload_to='./media/')
    tag = models.ManyToManyField(Tag, max_length=64)
    date_pub = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date_pub',)

    def __str__(self) -> str:
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт', related_name='ingredients_recipe')
    value = models.FloatField('Количество', max_length=32,
                              validators=[MinValueValidator(1)])

    def add_ingredient(self, recipe_id, title, amount):
        ingredient = get_object_or_404(Ingredient, title=title)
        return self.objects.get_or_create(recipe_id=recipe_id,
                                          ingredient=ingredient, amount=amount)

    class Meta:
        verbose_name_plural = 'Ингредиенты для рецепта'
        verbose_name = 'Ингредиент для рецепта'

    def __str__(self) -> str:
        return f'{self.ingredient.title} - {"%g" % self.value} {self.ingredient.dimension}'


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_follow')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['user', 'author']

    def __str__(self) -> str:
        return f'Автор - {self.author}, Подписчик - {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_sl',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_sl',
                               verbose_name='Рецепт')
    date_pub = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('-date_pub',)

    def __str__(self):
        return f'Пользователь - {self.user}, Рецепт - {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower_recipe',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='follow_recipe',
                               verbose_name='Рецепт')
    date_pub = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('-date_pub',)

    def __str__(self):
        return f'Пользователь - {self.user}, Рецепт - {self.recipe}'
