# Generated by Django 2.2.4 on 2019-09-17 19:14

import WhatToDo.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WhatToDo.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=30, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.TextField(max_length=50, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='province',
            field=models.CharField(blank=True, max_length=30, validators=[WhatToDo.validators.validate_characters], verbose_name='provice/state'),
        ),
        migrations.DeleteModel(
            name='EventComment',
        ),
    ]
