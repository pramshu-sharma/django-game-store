# Generated by Django 5.0.3 on 2024-03-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0018_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishlistUserGames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
