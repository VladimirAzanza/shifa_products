# Generated by Django 5.1.1 on 2024-11-18 18:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_category_options_alter_location_options_and_more'),
        ('orders', '0006_order_address'),
        ('users', '0002_addressuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Órden de compra', 'verbose_name_plural': 'Órdenes de compra'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Artículo en órden de compra', 'verbose_name_plural': 'Artículos en órden de compra'},
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pendiente'), ('PROCESSING', 'Procesando'), ('SHIPPED', 'Enviado'), ('DELIVERED', 'Entregado'), ('CANCELLED', 'Cancelado')], default='PROCESSING', max_length=20, verbose_name='Estado orden'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='users.addressuser', verbose_name='Dirección de entrega'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order', verbose_name='Órden de compra'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='catalog.product', verbose_name='Producto'),
        ),
    ]
