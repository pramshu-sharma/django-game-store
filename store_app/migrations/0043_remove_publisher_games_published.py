# Generated by Django 5.0.3 on 2024-04-02 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0042_delete_salepublisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='games_published',
        ),
    ]
