# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 01:47
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
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('data_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField()),
                ('published', models.CharField(blank=True, choices=[('pr', 'private'), ('sh', 'shared'), ('pu', 'public')], default='pr', max_length=2)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_photos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
