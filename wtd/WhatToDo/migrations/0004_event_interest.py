# Generated by Django 2.2.4 on 2019-09-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0003_auto_20190917_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='interest',
            field=models.ManyToManyField(blank=True, related_name='post_interest', to='WhatToDo.Profile'),
        ),
    ]
