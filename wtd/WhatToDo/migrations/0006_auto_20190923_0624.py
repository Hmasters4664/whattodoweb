# Generated by Django 2.2.4 on 2019-09-23 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0005_event_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
