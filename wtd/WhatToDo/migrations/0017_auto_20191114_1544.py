# Generated by Django 2.2.6 on 2019-11-14 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0016_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pcomments', to='WhatToDo.Post'),
        ),
    ]
