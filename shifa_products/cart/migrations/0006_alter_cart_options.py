# Generated by Django 5.1.1 on 2024-12-04 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-created_at'], 'verbose_name': 'Carrito de compra', 'verbose_name_plural': 'Carritos de compra'},
        ),
    ]