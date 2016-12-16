# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('twitter', models.CharField(max_length=15)),
                ('rating', models.IntegerField(default=0)),
                ('available', models.BooleanField(default=False)),
                ('thumbnail_price', models.FloatField()),
                ('channel_art_price', models.FloatField()),
                ('monthly', models.BooleanField(default=False)),
            ],
        ),
    ]
