# Generated by Django 2.2.4 on 2019-08-20 12:32

import WhatToDo.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='WhatToDo.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Organiser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
                ('phone', models.CharField(max_length=12, validators=[WhatToDo.validators.validate_characters])),
                ('facebookurl', models.CharField(max_length=50)),
                ('twitterhandle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('name', models.TextField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('province', models.CharField(blank=True, max_length=30, verbose_name='provice/state')),
                ('birth_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
                ('addressline1', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
                ('addressline2', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('country', models.CharField(max_length=50, validators=[WhatToDo.validators.validate_characters])),
                ('province', models.CharField(max_length=50, validators=[WhatToDo.validators.validate_characters], verbose_name='provice/state')),
                ('city', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Friends'), (2, 'Blocked')])),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to='WhatToDo.Profile')),
                ('to_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to='WhatToDo.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='relationships',
            field=models.ManyToManyField(through='WhatToDo.Relationship', to='WhatToDo.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[WhatToDo.validators.validate_characters])),
                ('description', models.TextField(validators=[WhatToDo.validators.validate_characters])),
                ('url', models.CharField(blank=True, max_length=50, verbose_name='Ticket Purchase URL')),
                ('imageUrl', models.CharField(max_length=50)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('lastModified', models.DateField(auto_now_add=True)),
                ('startDate', models.DateField(verbose_name='Start Date and Time')),
                ('endDate', models.DateField(verbose_name='End Date and Time')),
                ('TicketPrice1', models.DecimalField(decimal_places=2, default=200.0, max_digits=19, validators=[WhatToDo.validators.check_negative_number])),
                ('TicketPrice2', models.DecimalField(decimal_places=2, default=200.0, max_digits=19, validators=[WhatToDo.validators.check_negative_number])),
                ('TicketPrice3', models.DecimalField(decimal_places=2, default=200.0, max_digits=19, validators=[WhatToDo.validators.check_negative_number])),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WhatToDo.Category')),
                ('venue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='WhatToDo.Venue')),
            ],
        ),
    ]
