# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_create_imagerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateField(auto_now=True),
        ),
    ]
