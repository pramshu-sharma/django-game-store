# Generated by Django 5.0.3 on 2024-03-19 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0013_delete_category_delete_developer_delete_genre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('pass_test', models.CharField(max_length=150)),
            ],
        ),
    ]