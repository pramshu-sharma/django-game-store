# Generated by Django 5.0.3 on 2024-04-03 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0046_publishersale_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PublisherSale',
            new_name='SalePublisher',
        ),
    ]
