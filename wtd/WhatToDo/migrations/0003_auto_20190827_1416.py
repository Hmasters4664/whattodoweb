# Generated by Django 2.2.4 on 2019-08-27 14:16

import WhatToDo.validators
import autoslug.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WhatToDo', '0002_eventcomment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, validators=[WhatToDo.validators.validate_characters]),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
        migrations.AlterField(
            model_name='eventcomment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 27, 14, 16, 9, 935837, tzinfo=utc)),
        ),
    ]
