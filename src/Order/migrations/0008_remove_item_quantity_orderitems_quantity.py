# Generated by Django 5.1.2 on 2024-10-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0007_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
