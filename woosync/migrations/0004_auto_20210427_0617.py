# Generated by Django 3.2 on 2021-04-27 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('woosync', '0003_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='woo_id',
            new_name='customer_id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]
