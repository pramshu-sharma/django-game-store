# Generated by Django 5.0.3 on 2024-04-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0037_remove_salegenre_genre_id_delete_genre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher', models.CharField(max_length=200)),
                ('games_published', models.IntegerField(blank=True)),
                ('create_ts', models.DateTimeField(auto_now_add=True)),
                ('update_ts', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
