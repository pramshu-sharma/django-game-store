# Generated by Django 5.0.3 on 2024-03-25 10:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0022_delete_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_app_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.games', to_field='app_id')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'game_app_id')},
            },
        ),
    ]
