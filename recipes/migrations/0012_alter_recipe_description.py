# Generated by Django 3.2.3 on 2021-06-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20210615_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(
                blank=True,
                max_length=1000,
                verbose_name='Описание'),
        ),
    ]
