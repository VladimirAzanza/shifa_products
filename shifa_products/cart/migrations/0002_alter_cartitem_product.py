# Generated by Django 5.1.1 on 2024-09-30 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('catalog', '0004_alter_review_quality_stars_alter_review_taste_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='catalog.product'),
        ),
    ]