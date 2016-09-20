# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 06:35
from __future__ import unicode_literals

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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_type', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=200)),
                ('type_of_photography', models.CharField(max_length=200)),
                ('social_media', models.CharField(max_length=200)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
