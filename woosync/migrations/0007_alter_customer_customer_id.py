# Generated by Django 3.2 on 2021-04-27 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woosync', '0006_rename_billing_post_code_customer_billing_postcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
