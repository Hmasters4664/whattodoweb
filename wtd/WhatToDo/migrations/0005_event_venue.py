# Generated by Django 2.2.4 on 2019-09-23 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0004_event_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WhatToDo.Venue'),
        ),
    ]