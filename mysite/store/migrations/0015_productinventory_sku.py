# Generated by Django 3.2.7 on 2021-09-25 09:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_productinventory_combination_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinventory',
            name='sku',
            field=models.CharField(default=datetime.datetime(2021, 9, 25, 9, 15, 37, 955371, tzinfo=utc), max_length=150),
            preserve_default=False,
        ),
    ]