# Generated by Django 3.2.3 on 2021-06-14 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_rename_name_ingredient_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredient',
            new_name='Ingredients',
        ),
    ]
