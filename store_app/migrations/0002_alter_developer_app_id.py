# Generated by Django 5.0.3 on 2024-03-14 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='app_id',
            field=models.IntegerField(),
        ),
    ]
