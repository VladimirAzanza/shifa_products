# Generated by Django 5.1.1 on 2024-10-08 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitem_cart_alter_cartitem_quantity'),
        ('orders', '0002_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.cart'),
        ),
    ]