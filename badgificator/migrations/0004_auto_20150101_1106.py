# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgificator', '0003_auto_20141219_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='simple_condition',
        ),
        migrations.AddField(
            model_name='badge',
            name='condition_type',
            field=models.CharField(default='', max_length=10, verbose_name='Type of condition for the badge', blank=True, choices=[('NRM', 'Number of models related to a user'), ('NCD', 'Number of consecutive days of presence'), ('ND', 'Number of days of presence'), ('NHFV', 'Number of hits for a view')]),
            preserve_default=False,
        ),
    ]
