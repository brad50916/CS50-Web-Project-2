# Generated by Django 4.1.4 on 2022-12-25 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_list_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='price',
        ),
    ]
