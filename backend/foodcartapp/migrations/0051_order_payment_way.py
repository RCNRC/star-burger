# Generated by Django 3.2.15 on 2023-07-03 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_auto_20230703_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_way',
            field=models.CharField(choices=[('ON', 'Онлайн'), ('OF', 'Наличными')], db_index=True, default='ON', max_length=2, verbose_name='способ оплаты'),
        ),
    ]
