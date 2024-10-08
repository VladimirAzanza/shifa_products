# Generated by Django 5.1.1 on 2024-10-08 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_address_remove_order_cart_items_and_more'),
        ('users', '0002_addressuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='users.addressuser'),
        ),
    ]
