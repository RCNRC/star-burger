# Generated by Django 3.2.15 on 2023-07-03 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_auto_20230703_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliver_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phoned_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время звонка'),
        ),
    ]
