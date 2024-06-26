# Generated by Django 5.0.3 on 2024-03-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0006_alter_category_category_alter_developer_developer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='achievements',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='description_long',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='description_short',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='dlc_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='image_main',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='peak_player_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='recommendations',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='release_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='required_age',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='reviews_negative',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='reviews_positive',
            field=models.IntegerField(null=True),
        ),
    ]
