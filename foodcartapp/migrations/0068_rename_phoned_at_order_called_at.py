# Generated by Django 3.2.15 on 2023-07-18 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0067_auto_20230718_2009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phoned_at',
            new_name='called_at',
        ),
    ]
