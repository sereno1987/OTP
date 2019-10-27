# Generated by Django 2.2.6 on 2019-10-25 17:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OTPAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneotp',
            name='phone',
            field=models.IntegerField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number'),
        ),
    ]
