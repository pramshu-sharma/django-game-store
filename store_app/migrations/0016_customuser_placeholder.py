# Generated by Django 5.0.3 on 2024-03-20 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0015_delete_testpost_remove_customuser_placeholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='placeholder',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]