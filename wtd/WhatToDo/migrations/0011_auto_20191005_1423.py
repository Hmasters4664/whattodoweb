# Generated by Django 2.2.4 on 2019-10-05 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0010_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='day',
        ),
        migrations.AddField(
            model_name='schedule',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]