# Generated by Django 5.0.3 on 2024-03-26 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0032_delete_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='release_date',
        ),
    ]
