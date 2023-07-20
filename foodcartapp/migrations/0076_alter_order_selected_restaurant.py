# Generated by Django 3.2.15 on 2023-07-20 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0075_alter_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='selected_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_items', to='foodcartapp.restaurant', verbose_name='выбранный ресторан'),
        ),
    ]
