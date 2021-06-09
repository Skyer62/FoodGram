from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                try:
                    name, unit = row
                    Ingredient.objects.get_or_create(name=name, unit=unit)
                except:
                    return 'Data have bad format'
            print('Data is loaded')