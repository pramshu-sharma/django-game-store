# Generated by Django 5.0.3 on 2024-04-02 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0039_publishersale'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PublisherSale',
            new_name='SalePublisher',
        ),
    ]