# Generated by Django 3.2.15 on 2023-06-12 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказы', 'verbose_name_plural': 'заказы'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='adress',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='second_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phonenumber',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.product', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.order', verbose_name='товар'),
        ),
    ]
