from django.forms import ModelForm
from django import forms
from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name="slug", required=False)
    class Meta:
        model = Recipe
        fields = ("title", "cooking_time", "description",  "image")
