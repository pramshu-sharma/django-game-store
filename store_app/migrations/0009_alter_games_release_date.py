# Generated by Django 5.0.3 on 2024-03-14 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0008_games_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='release_date',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
