# Generated by Django 3.2.7 on 2021-09-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_customer_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='marked_price',
            field=models.FloatField(),
        ),
    ]
