# Generated by Django 3.2.7 on 2021-09-25 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_productvariationsoptions_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariationsoptions',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]