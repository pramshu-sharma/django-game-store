# Generated by Django 5.0.3 on 2024-03-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0016_customuser_placeholder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='placeholder',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
