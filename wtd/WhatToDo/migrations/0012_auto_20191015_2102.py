# Generated by Django 2.2.4 on 2019-10-15 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0011_auto_20191005_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_medium',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_small',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]