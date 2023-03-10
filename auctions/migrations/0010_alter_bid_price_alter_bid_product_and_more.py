# Generated by Django 4.1.4 on 2022-12-21 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_list_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Bid', to='auctions.list'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='auctions.list'),
        ),
    ]
