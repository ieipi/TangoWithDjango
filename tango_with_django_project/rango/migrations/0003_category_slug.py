# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20150517_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            #field=models.SlugField(default='', unique=True),
            field=models.SlugField(null = True),
            preserve_default=False,
        ),
    ]
