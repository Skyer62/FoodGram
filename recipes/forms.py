from django import forms
from django.core import validators

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name='slug', required=False)
    cooking_time = forms.IntegerField(validators=[validators.validate_integer])

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image')
