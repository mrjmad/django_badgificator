# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgificator', '0002_auto_20141219_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='name_field',
        ),
        migrations.AddField(
            model_name='badge',
            name='name_for_check',
            field=models.CharField(default="", max_length=100, verbose_name='Name of Field or View for check for simple condition', blank=True),
            preserve_default=False,
        ),
    ]
