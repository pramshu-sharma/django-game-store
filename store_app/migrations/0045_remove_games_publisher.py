# Generated by Django 5.0.3 on 2024-04-02 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0044_publishergame'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='publisher',
        ),
    ]
