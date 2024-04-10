# Generated by Django 5.0.3 on 2024-03-14 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_delete_developer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='publisher',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='screenshot',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.CharField(max_length=1000, null=True)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.games')),
            ],
        ),
    ]